'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Trash2, ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useChat } from '@/hooks/useChat';
import type { ChatMode } from '@/lib/types';

interface AIChatCardProps {
    className?: string;
    onClose?: () => void;
}

export default function AIChatCard({ className, onClose }: AIChatCardProps) {
    const { messages, loading, mode, setMode, sendMessage, clearChat } = useChat();
    const [input, setInput] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll к последнему сообщению
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || loading) return;
        const messageText = input;
        setInput('');
        await sendMessage(messageText);
    };

    const handleClearChat = async () => {
        if (confirm('Очистить историю чата?')) {
            await clearChat();
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className={cn('relative h-[700px] w-[500px] rounded-2xl p-[2px]', className)}>
            {/* Animated Outer Border */}
            <motion.div
                className="absolute inset-0 rounded-2xl border-2 border-purple-300/50"
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 25, repeat: Infinity, ease: 'linear' }}
            />

            {/* Inner Card */}
            <div className="relative flex h-full w-full flex-col rounded-xl border border-purple-200 bg-white backdrop-blur-xl">
                {/* Inner Animated Background */}
                <motion.div
                    className="absolute inset-0 bg-gradient-to-br from-purple-50 via-white to-blue-50"
                    animate={{ backgroundPosition: ['0% 0%', '100% 100%', '0% 0%'] }}
                    transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
                    style={{ backgroundSize: '200% 200%' }}
                />

                {/* Floating Particles */}
                {Array.from({ length: 15 }).map((_, i) => (
                    <motion.div
                        key={i}
                        className="absolute h-1 w-1 rounded-full bg-purple-300/40"
                        animate={{
                            y: ['0%', '-140%'],
                            x: [Math.random() * 200 - 100, Math.random() * 200 - 100],
                            opacity: [0, 1, 0],
                        }}
                        transition={{
                            duration: 5 + Math.random() * 3,
                            repeat: Infinity,
                            delay: i * 0.5,
                            ease: 'easeInOut',
                        }}
                        style={{ left: `${Math.random() * 100}%`, bottom: '-10%' }}
                    />
                ))}

                {/* Header */}
                <div className="relative z-10 border-b border-purple-200 px-6 py-8">
                    <div className="flex items-start justify-between gap-4 mb-4">
                        <div className="flex-1">
                            <h2 className="text-3xl font-bold text-purple-900 mb-3">🎵 Музыкальный консультант</h2>
                            <p className="text-base text-gray-700 mb-2 leading-relaxed">
                                Помогу подобрать идеальную музыку под любое настроение и ситуацию
                            </p>
                            <div className="flex flex-wrap gap-2 mb-2">
                                <span className="inline-flex items-center rounded-full bg-purple-100 px-2.5 py-0.5 text-xs font-medium text-purple-800">
                                    🎸 Жанры
                                </span>
                                <span className="inline-flex items-center rounded-full bg-purple-100 px-2.5 py-0.5 text-xs font-medium text-purple-800">
                                    🎧 Плейлисты
                                </span>
                                <span className="inline-flex items-center rounded-full bg-purple-100 px-2.5 py-0.5 text-xs font-medium text-purple-800">
                                    🎤 Артисты
                                </span>
                            </div>
                            <p className="text-xs text-gray-500">
                                Режим: {mode === 'normal' ? '💬 Обычный' : '📊 Администратор'}
                            </p>
                        </div>
                        <div className="flex flex-col gap-2">
                            {/* Mode Toggle */}
                            <button
                                onClick={() => setMode(mode === 'normal' ? 'admin' : 'normal')}
                                className="rounded-lg bg-purple-100 px-3 py-1.5 text-xs text-purple-900 transition-colors hover:bg-purple-200"
                                title="Переключить режим"
                            >
                                {mode === 'normal' ? '📊 Admin' : '💬 Normal'}
                            </button>
                            {/* Clear Chat */}
                            <button
                                onClick={handleClearChat}
                                className="rounded-lg bg-purple-100 p-2 text-purple-900 transition-colors hover:bg-purple-200"
                                title="Очистить чат"
                            >
                                <Trash2 className="h-4 w-4" />
                            </button>
                        </div>
                    </div>
                </div>

                {/* Messages */}
                <div className="relative z-10 flex flex-1 flex-col space-y-3 overflow-y-auto px-4 py-2 text-sm">
                    <AnimatePresence>
                        {messages.map((msg, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0 }}
                                transition={{ duration: 0.4 }}
                                className="flex flex-col"
                            >
                                <div
                                    className={cn(
                                        'max-w-[85%] rounded-xl px-3 py-2 shadow-md backdrop-blur-md',
                                        msg.role === 'assistant'
                                            ? 'self-start bg-purple-100 text-gray-900'
                                            : 'self-end bg-purple-500 font-semibold text-white'
                                    )}
                                >
                                    {msg.content}
                                </div>

                                {/* SQL Query Display (только в admin режиме) */}
                                {msg.sql_query && msg.role === 'assistant' && (
                                    <details className="mt-1 max-w-[85%] self-start">
                                        <summary className="cursor-pointer text-xs text-gray-600 hover:text-gray-700">
                                            <ChevronDown className="inline h-3 w-3" /> SQL запрос
                                        </summary>
                                        <pre className="mt-1 overflow-x-auto rounded bg-gray-100 p-2 text-xs text-green-700">
                                            {msg.sql_query}
                                        </pre>
                                    </details>
                                )}
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {/* AI Typing Indicator */}
                    {loading && (
                        <motion.div
                            className="flex max-w-[30%] items-center gap-1 self-start rounded-xl bg-purple-100 px-3 py-2"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: [0, 1, 0.6, 1] }}
                            transition={{ repeat: Infinity, duration: 1.2 }}
                        >
                            <span className="h-2 w-2 animate-pulse rounded-full bg-purple-500"></span>
                            <span
                                className="h-2 w-2 animate-pulse rounded-full bg-purple-500"
                                style={{ animationDelay: '0.2s' }}
                            ></span>
                            <span
                                className="h-2 w-2 animate-pulse rounded-full bg-purple-500"
                                style={{ animationDelay: '0.4s' }}
                            ></span>
                        </motion.div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <div className="relative z-10 flex items-center gap-2 border-t border-purple-200 p-4">
                    <input
                        className="flex-1 rounded-lg border border-purple-200 bg-white px-3 py-2 text-sm text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-400"
                        placeholder="Напишите сообщение..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={loading}
                    />
                    <button
                        onClick={handleSend}
                        disabled={loading || !input.trim()}
                        className="rounded-lg bg-purple-500 p-2 transition-colors hover:bg-purple-600 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        <Send className="h-4 w-4 text-white" />
                    </button>
                </div>
            </div>
        </div>
    );
}
