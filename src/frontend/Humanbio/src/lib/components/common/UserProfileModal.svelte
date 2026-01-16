<script>
    import { API_URL } from "$lib/constants";
    import Avatar from "$lib/components/common/Avatar.svelte";
    import { fade, scale } from "svelte/transition";
    import { viewedUserId } from "$lib/stores/ui";

    let user = $state(null);
    let loading = $state(false);
    let isOpen = $state(false);

    // Subscribe to store manually or use $effect with auto-subscription $viewedUserId
    // Using effect is better in Svelte 5
    $effect(() => {
        if ($viewedUserId) {
            isOpen = true;
            loadUser($viewedUserId);
        } else {
            isOpen = false;
            user = null;
        }
    });

    function close() {
        viewedUserId.set(null);
    }

    async function loadUser(id) {
        loading = true;
        user = null; // Clear previous user
        try {
            const res = await fetch(`${API_URL}/api/users/${id}`);
            if (res.ok) {
                user = await res.json();
            }
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }
</script>

{#if isOpen}
    <div class="fixed inset-0 z-[150] flex items-center justify-center p-4">
        <!-- Backdrop -->
        <button
            type="button"
            class="absolute inset-0 bg-black/60 backdrop-blur-md cursor-default w-full h-full border-none"
            onclick={close}
            transition:fade={{ duration: 200 }}
            aria-label="Close"
        ></button>

        <!-- Modal -->
        <div
            class="relative w-full max-w-sm bg-fd-card border border-fd-border rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
            transition:scale={{ duration: 300, start: 0.95 }}
        >
            <div
                class="relative bg-fd-accent/30 p-6 flex flex-col items-center border-b border-fd-border/50"
            >
                <button
                    onclick={close}
                    class="absolute top-4 right-4 text-fd-muted hover:text-fd-foreground transition-colors"
                >
                    <i class="bx bx-x text-2xl"></i>
                </button>

                {#if loading}
                    <div class="py-10">
                        <i
                            class="bx bx-loader-alt animate-spin text-3xl text-fd-primary"
                        ></i>
                    </div>
                {:else if user}
                    <Avatar
                        url={user.avatar_url}
                        seed={user.avatar_seed || user.username}
                        size={80}
                        class="rounded-2xl shadow-lg mb-4"
                    />

                    <h2
                        class="text-xl font-black text-fd-foreground tracking-tight"
                    >
                        {user.username}
                    </h2>

                    {#if user.is_admin}
                        <div
                            class="mt-2 flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-fd-primary/10 border border-fd-primary/20"
                        >
                            <i
                                class="bx bxs-badge-check text-fd-primary text-xs"
                            ></i>
                            <span
                                class="text-[10px] font-bold text-fd-primary uppercase tracking-widest"
                                >Admin</span
                            >
                        </div>
                    {:else}
                        <span
                            class="text-[10px] font-bold text-fd-muted uppercase tracking-widest mt-1"
                            >Thành viên</span
                        >
                    {/if}
                {:else}
                    <div class="text-center py-10">
                        <i class="bx bx-error text-3xl text-red-500 mb-2"></i>
                        <p class="text-sm font-bold text-fd-foreground">
                            Không tìm thấy người dùng
                        </p>
                    </div>
                {/if}
            </div>

            {#if user && !loading}
                <div class="p-6 overflow-y-auto space-y-6">
                    {#if user.bio}
                        <div class="space-y-2 text-center">
                            <p
                                class="text-sm text-fd-foreground/80 leading-relaxed whitespace-pre-wrap"
                            >
                                {user.bio}
                            </p>
                        </div>
                    {:else}
                        <p class="text-xs text-fd-muted text-center italic">
                            Chưa có giới thiệu.
                        </p>
                    {/if}

                    {#if user.social_links && Object.keys(user.social_links).length > 0}
                        <div class="space-y-3">
                            <h3
                                class="text-[10px] font-black uppercase tracking-widest text-fd-muted text-center"
                            >
                                Liên kết
                            </h3>
                            <div class="grid grid-cols-1 gap-2">
                                {#each Object.entries(user.social_links) as [title, url]}
                                    <a
                                        href={url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        class="flex items-center justify-between px-4 py-3 rounded-xl bg-fd-secondary/50 hover:bg-fd-accent border border-fd-border/50 hover:border-fd-primary/30 transition-all group"
                                    >
                                        <span
                                            class="text-xs font-bold text-fd-foreground group-hover:text-fd-primary transition-colors"
                                            >{title}</span
                                        >
                                        <i
                                            class="bx bx-link-external text-fd-muted text-sm group-hover:text-fd-primary"
                                        ></i>
                                    </a>
                                {/each}
                            </div>
                        </div>
                    {/if}
                </div>
            {/if}
        </div>
    </div>
{/if}
