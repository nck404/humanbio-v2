import { writable } from 'svelte/store';

export const isChatOpen = writable(false);
export const isSearchOpen = writable(false);
export const viewedUserId = writable(null);
