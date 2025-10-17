/**
 * Утилиты для форматирования дат, чисел и текста
 */

import { format, formatDistanceToNow, parseISO } from 'date-fns';
import { ru } from 'date-fns/locale';

/**
 * Форматирует ISO дату в читаемый формат
 * @param isoString - дата в формате ISO 8601
 * @returns отформатированная дата (например, "17 окт 2025, 18:30")
 */
export function formatDate(isoString: string): string {
    try {
        return format(parseISO(isoString), 'dd MMM yyyy, HH:mm', { locale: ru });
    } catch (error) {
        console.error('Error formatting date:', error);
        return isoString;
    }
}

/**
 * Форматирует дату в относительное время
 * @param isoString - дата в формате ISO 8601
 * @returns относительное время (например, "2 часа назад")
 */
export function formatRelativeTime(isoString: string): string {
    try {
        return formatDistanceToNow(parseISO(isoString), {
            addSuffix: true,
            locale: ru,
        });
    } catch (error) {
        console.error('Error formatting relative time:', error);
        return isoString;
    }
}

/**
 * Форматирует число с разделителями тысяч
 * @param num - число для форматирования
 * @returns отформатированное число (например, "1 234")
 */
export function formatNumber(num: number): string {
    return new Intl.NumberFormat('ru-RU').format(num);
}

/**
 * Обрезает текст до указанной длины с добавлением многоточия
 * @param text - исходный текст
 * @param maxLength - максимальная длина
 * @returns обрезанный текст с "..." если превышена длина
 */
export function truncateText(text: string, maxLength: number): string {
    if (text.length <= maxLength) {
        return text;
    }
    return text.slice(0, maxLength) + '...';
}

/**
 * Форматирует дробное число с фиксированным количеством знаков после запятой
 * @param num - число
 * @param decimals - количество знаков после запятой
 * @returns отформатированное число
 */
export function formatDecimal(num: number, decimals: number = 1): string {
    return num.toFixed(decimals);
}
