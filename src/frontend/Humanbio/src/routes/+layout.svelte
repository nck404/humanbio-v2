<script>
	import "./layout.css";
	import favicon from "$lib/assets/favicon.svg";
	import Navbar from "$lib/components/Navbar.svelte";
	import { auth } from "$lib/stores/auth";
	import { page } from "$app/stores";
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";

	import { settings } from "$lib/stores/settings";
	import { API_URL } from "$lib/constants";

	let { children } = $props();

	// Protection logic
	$effect(() => {
		const path = $page.url.pathname;
		const isAuthPath = ["/login", "/register"].includes(path);
		const isAdminPath = path.startsWith("/admin");

		if (!isAuthPath && !$auth.isAuthenticated) {
			goto("/login");
		} else if (isAuthPath && $auth.isAuthenticated) {
			goto("/");
		} else if (isAdminPath && !$auth.user?.is_admin) {
			goto("/");
		}
	});

	onMount(async () => {
		if ($auth.isAuthenticated) {
			try {
				const res = await fetch(`${API_URL}/api/me`, {
					headers: {
						Authorization: `Bearer ${$auth.token}`,
					},
				});
				if (res.ok) {
					const data = await res.json();
					if (data.settings) {
						settings.update((s) => ({
							...s,
							...data.settings,
							theme: "light",
						}));
					}
				}
			} catch (e) {
				console.error("Failed to load user settings", e);
			}
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div
	class="min-h-screen bg-fd-background text-fd-foreground flex flex-col transition-all duration-500"
	data-theme={$settings.theme}
	style="
        --primary-color: {$settings.primaryColor}; 
        font-family: var(--font-{$settings.fontFamily || 'sans'});
    "
>
	<Navbar />
	<main class="flex-grow">
		{@render children()}
	</main>
</div>
