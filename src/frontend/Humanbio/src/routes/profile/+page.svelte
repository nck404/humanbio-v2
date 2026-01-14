<script>
    import { onMount } from "svelte";
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import { API_URL } from "$lib/constants";

    let userProfile = null;
    let loading = true;
    let error = "";

    onMount(async () => {
        if (!$auth.isAuthenticated) {
            goto("/login");
            return;
        }

        try {
            const response = await fetch(`${API_URL}/api/me`, {
                headers: {
                    Authorization: `Bearer ${$auth.token}`,
                },
            });

            if (response.ok) {
                userProfile = await response.json();
            } else {
                error = "Failed to load profile. session may have expired.";
                // If unauthorized, logout
                if (response.status === 401) {
                    auth.set({
                        token: null,
                        user: null,
                        isAuthenticated: false,
                    });
                    goto("/login");
                }
            }
        } catch (e) {
            error = "Could not connect to server";
        } finally {
            loading = false;
        }
    });
</script>

<div class="max-w-[800px] mx-auto py-16 px-6">
    <header class="mb-12">
        <h1
            class="text-4xl font-extrabold text-fd-foreground tracking-tight mb-3"
        >
            Account Settings
        </h1>
        <p class="text-fd-muted font-medium">
            Manage your personal information and security preferences.
        </p>
    </header>

    <div class="space-y-8">
        {#if loading}
            <div class="flex justify-center py-20">
                <i
                    class="bx bx-loader-alt animate-spin text-4xl text-fd-primary"
                ></i>
            </div>
        {:else}
            <div class="fd-card p-1">
                <div
                    class="bg-fd-accent/50 p-8 rounded-[0.7rem] flex flex-col md:flex-row items-center gap-8 border-b border-fd-border/50"
                >
                    <div
                        class="w-24 h-24 bg-fd-primary/20 rounded-2xl flex items-center justify-center text-fd-primary text-4xl shadow-inner border border-fd-primary/20"
                    >
                        <i class="bx bx-user-circle"></i>
                    </div>
                    <div class="text-center md:text-left space-y-1">
                        <h2 class="text-2xl font-bold text-fd-foreground">
                            {userProfile?.username}
                        </h2>
                        <p
                            class="text-fd-muted flex items-center gap-2 justify-center md:justify-start"
                        >
                            <i class="bx bx-envelope"></i>
                            {userProfile?.email}
                        </p>
                        <div class="pt-2">
                            <span
                                class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full {userProfile?.is_admin
                                    ? 'bg-fd-primary/20 text-fd-primary border border-fd-primary/30'
                                    : 'bg-fd-secondary text-fd-muted border border-fd-border'}"
                            >
                                {userProfile?.is_admin
                                    ? "Administrator"
                                    : "Standard Member"}
                            </span>
                        </div>
                    </div>
                </div>

                <div class="p-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="space-y-4">
                        <h3
                            class="text-sm font-bold text-fd-foreground flex items-center gap-2"
                        >
                            <i class="bx bx-id-card text-fd-primary"></i>
                            Personal Details
                        </h3>
                        <div class="space-y-3">
                            <div
                                class="p-4 bg-fd-background/50 rounded-xl border border-fd-border"
                            >
                                <p
                                    class="text-[10px] text-fd-muted-foreground uppercase font-bold tracking-tighter mb-1"
                                >
                                    Internal User ID
                                </p>
                                <p class="text-xs font-mono text-fd-muted">
                                    #{userProfile?.id}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div class="space-y-4">
                        <h3
                            class="text-sm font-bold text-fd-foreground flex items-center gap-2"
                        >
                            <i class="bx bx-shield-check text-fd-primary"></i>
                            Security Status
                        </h3>
                        <div class="space-y-3">
                            <div
                                class="p-4 bg-fd-background/50 rounded-xl border border-fd-border"
                            >
                                <p
                                    class="text-[10px] text-fd-muted-foreground uppercase font-bold tracking-tighter mb-1"
                                >
                                    Account Protection
                                </p>
                                <p
                                    class="text-xs font-medium text-emerald-400 flex items-center gap-2"
                                >
                                    <span
                                        class="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"
                                    ></span>
                                    Verified & Active
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex justify-end gap-3 mt-4">
                <button
                    class="px-4 py-2 text-xs font-semibold text-fd-muted hover:text-fd-foreground transition-colors"
                >
                    Reset Password
                </button>
                <button
                    class="px-5 py-2.5 text-xs font-bold bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white rounded-lg border border-red-500/20 transition-all"
                >
                    Deactivate Account
                </button>
            </div>
        {/if}

        {#if error}
            <div
                class="mt-4 p-4 bg-red-900/20 border border-red-900/50 rounded-xl text-red-400 text-center text-sm"
            >
                {error}
            </div>
        {/if}
    </div>
</div>
