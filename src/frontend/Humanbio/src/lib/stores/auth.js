import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const initialToken = browser ? localStorage.getItem('token') : null;
const initialUser = browser ? JSON.parse(localStorage.getItem('user') || 'null') : null;

export const auth = writable({
    token: initialToken,
    user: initialUser,
    isAuthenticated: !!initialToken
});

if (browser) {
    auth.subscribe(value => {
        if (value.token) {
            localStorage.setItem('token', value.token);
            localStorage.setItem('user', JSON.stringify(value.user));
        } else {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
        }
    });
}

export const logout = () => {
    auth.set({
        token: null,
        user: null,
        isAuthenticated: false
    });
};
