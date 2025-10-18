'use client';

import { useState } from 'react';
import { MessageCircle, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import AIChatCard from '@/components/ui/ai-chat';

/**
 * Floating Chat Button - кнопка для открытия чата в правом нижнем углу
 */
export function FloatingChatButton() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            {/* Floating Button */}
            <motion.button
                className="fixed bottom-6 right-6 z-50 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 p-4 text-white shadow-2xl transition-transform hover:scale-110"
                onClick={() => setIsOpen(!isOpen)}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                title={isOpen ? 'Закрыть чат' : 'Открыть чат с музыкальным консультантом'}
            >
                <AnimatePresence mode="wait">
                    {isOpen ? (
                        <motion.div
                            key="close"
                            initial={{ rotate: -90, opacity: 0 }}
                            animate={{ rotate: 0, opacity: 1 }}
                            exit={{ rotate: 90, opacity: 0 }}
                            transition={{ duration: 0.2 }}
                        >
                            <X className="h-6 w-6" />
                        </motion.div>
                    ) : (
                        <motion.div
                            key="open"
                            initial={{ rotate: 90, opacity: 0 }}
                            animate={{ rotate: 0, opacity: 1 }}
                            exit={{ rotate: -90, opacity: 0 }}
                            transition={{ duration: 0.2 }}
                        >
                            <MessageCircle className="h-6 w-6" />
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Notification Badge (опционально, для будущего) */}
                {/* <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-xs font-bold">
          3
        </span> */}
            </motion.button>

            {/* Chat Popover */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 20, scale: 0.95 }}
                        transition={{ duration: 0.3, ease: 'easeOut' }}
                        className="fixed bottom-24 right-6 z-50"
                    >
                        <AIChatCard onClose={() => setIsOpen(false)} />
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
}
