import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const defaultSettings = {
    theme: 'light',
    fontSize: 16,
    fontFamily: 'sans',
    primaryColor: '#6366f1'
};

const initialSettings = browser ? (JSON.parse(localStorage.getItem('appSettings')) || defaultSettings) : defaultSettings;

// Force light mode as per user request
initialSettings.theme = 'light';
if (!initialSettings.primaryColor) initialSettings.primaryColor = '#6366f1';

export const settings = writable(initialSettings);

if (browser) {
    settings.subscribe(value => {
        // Force light mode in state if it somehow gets changed
        if (value.theme !== 'light') {
            value.theme = 'light';
        }
        
        localStorage.setItem('appSettings', JSON.stringify(value));
        document.documentElement.setAttribute('data-theme', 'light');
        document.documentElement.style.fontSize = `${value.fontSize}px`;
        document.documentElement.style.setProperty('--primary-color', value.primaryColor);
        
        // Split hex to HSL for some legacy components if needed, 
        // but it's better to use the color directly.
        // For now, let's just use the color.
        
        // Update font family classes on body
        const bodies = document.querySelectorAll('body');
        bodies.forEach(body => {
            body.classList.remove('font-sans', 'font-serif', 'font-mono');
            body.classList.add(`font-${value.fontFamily}`);
        });
    });
}
