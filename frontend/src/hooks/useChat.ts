/**
 * Custom hook для управления состоянием чата
 *
 * Обеспечивает:
 * - Управление сообщениями
 * - Отправку сообщений через API
 * - Переключение режимов (normal/admin)
 * - Persistence session_id в localStorage
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { apiClient } from '@/lib/api';
import type { ChatMessage, ChatMode } from '@/lib/types';

const SESSION_STORAGE_KEY = 'chat_session_id';

interface UseChatReturn {
    messages: ChatMessage[];
    loading: boolean;
    error: string | null;
    mode: ChatMode;
    sessionId: string | null;
    sendMessage: (message: string) => Promise<void>;
    clearChat: () => Promise<void>;
    setMode: (mode: ChatMode) => void;
}

/**
 * Hook для работы с чатом
 */
export function useChat(): UseChatReturn {
    const [messages, setMessages] = useState<ChatMessage[]>([
        {
            role: 'assistant',
            content: '👋 Привет! Я ваш AI-ассистент. Чем могу помочь?',
        },
    ]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [mode, setMode] = useState<ChatMode>('normal');
    const [sessionId, setSessionId] = useState<string | null>(null);
    const isInitialized = useRef(false);

    // Инициализация: получить или создать session ID
    useEffect(() => {
        if (isInitialized.current) return;
        isInitialized.current = true;

        const initSession = async () => {
            // Попытка получить из localStorage
            const storedSessionId = localStorage.getItem(SESSION_STORAGE_KEY);

            if (storedSessionId) {
                setSessionId(storedSessionId);
            } else {
                // Создать новый session ID
                try {
                    const { session_id } = await apiClient.getOrCreateSession();
                    setSessionId(session_id);
                    localStorage.setItem(SESSION_STORAGE_KEY, session_id);
                } catch (err) {
                    console.error('Failed to create session:', err);
                    // Fallback: генерация на клиенте
                    const fallbackId = `web_${crypto.randomUUID()}`;
                    setSessionId(fallbackId);
                    localStorage.setItem(SESSION_STORAGE_KEY, fallbackId);
                }
            }
        };

        initSession();
    }, []);

    /**
     * Отправка сообщения в чат
     */
    const sendMessage = useCallback(
        async (message: string) => {
            if (!message.trim() || !sessionId) return;

            setError(null);
            setLoading(true);

            // Добавить сообщение пользователя
            const userMessage: ChatMessage = {
                role: 'user',
                content: message,
                timestamp: new Date().toISOString(),
            };
            setMessages((prev) => [...prev, userMessage]);

            try {
                // Отправить запрос к API
                const response = await apiClient.sendChatMessage({
                    message,
                    mode,
                    session_id: sessionId,
                });

                // Добавить ответ ассистента
                const assistantMessage: ChatMessage = {
                    role: 'assistant',
                    content: response.message,
                    sql_query: response.sql_query,
                    timestamp: new Date().toISOString(),
                };
                setMessages((prev) => [...prev, assistantMessage]);
            } catch (err) {
                console.error('Failed to send message:', err);
                const errorMessage =
                    err instanceof Error ? err.message : 'Не удалось отправить сообщение. Попробуйте позже.';
                setError(errorMessage);

                // Добавить сообщение об ошибке
                const errorAssistantMessage: ChatMessage = {
                    role: 'assistant',
                    content: `❌ Ошибка: ${errorMessage}`,
                    timestamp: new Date().toISOString(),
                };
                setMessages((prev) => [...prev, errorAssistantMessage]);
            } finally {
                setLoading(false);
            }
        },
        [mode, sessionId]
    );

    /**
     * Очистка истории чата
     */
    const clearChat = useCallback(async () => {
        if (!sessionId) return;

        setLoading(true);
        setError(null);

        try {
            await apiClient.clearChat(sessionId);

            // Сбросить сообщения к начальному состоянию
            setMessages([
                {
                    role: 'assistant',
                    content: '👋 Привет! Я ваш AI-ассистент. Чем могу помочь?',
                },
            ]);
        } catch (err) {
            console.error('Failed to clear chat:', err);
            const errorMessage = err instanceof Error ? err.message : 'Не удалось очистить историю';
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    }, [sessionId]);

    return {
        messages,
        loading,
        error,
        mode,
        sessionId,
        sendMessage,
        clearChat,
        setMode,
    };
}
