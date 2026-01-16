<script>
    import { onMount } from "svelte";
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import { API_URL } from "$lib/constants";
    import Avatar from "$lib/components/common/Avatar.svelte";
    import { fade } from "svelte/transition";

    let userProfile = $state(null);
    let loading = $state(true);
    let error = $state("");
    let savingAvatar = $state(false);
    let successMsg = $state("");

    // Avatar state
    let avatarSeed = $state("");
    let fileInput = $state();
    let uploadingFile = $state(false);

    // Profile Info State
    let bio = $state("");
    let linksList = $state([]);
    let savingProfile = $state(false);

    onMount(async () => {
        if (!$auth.isAuthenticated) {
            goto("/login");
            return;
        }

        await loadProfile();
    });

    async function loadProfile() {
        try {
            const response = await fetch(`${API_URL}/api/me`, {
                headers: {
                    Authorization: `Bearer ${$auth.token}`,
                },
            });

            if (response.ok) {
                userProfile = await response.json();
                userProfile = await response.json();
                avatarSeed = userProfile.avatar_seed || "";
                bio = userProfile.bio || "";

                // Convert dict to list for easier editing
                linksList = [];
                if (userProfile.social_links) {
                    for (const [key, value] of Object.entries(
                        userProfile.social_links,
                    )) {
                        linksList.push({
                            title: key,
                            url: value,
                            id: Math.random().toString(36).substr(2, 9),
                        });
                    }
                }
            } else {
                error = "Failed to load profile. session may have expired.";
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
    }

    function randomizeAvatar() {
        userProfile.avatar_url = null; // Clear custom URL when randomizing
        avatarSeed = Math.random().toString(36).substring(7);
    }

    async function saveAvatar() {
        if (savingAvatar) return;

        // If we have a URL and the seed is empty (meaning we just uploaded), don't overwrite
        if (userProfile.avatar_url && !avatarSeed) {
            return;
        }

        savingAvatar = true;
        error = "";
        successMsg = "";

        try {
            const response = await fetch(`${API_URL}/api/me/avatar`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${$auth.token}`,
                },
                body: JSON.stringify({ avatar_seed: avatarSeed }),
            });

            if (response.ok) {
                successMsg = "Cập nhật ảnh đại diện thành công!";
                userProfile.avatar_seed = avatarSeed;
                userProfile.avatar_url = null;

                const updatedUser = {
                    ...$auth.user,
                    avatar_seed: avatarSeed,
                    avatar_url: null,
                };
                auth.update((curr) => ({ ...curr, user: updatedUser }));

                setTimeout(() => (successMsg = ""), 3000);
            } else {
                error = "Không thể cập nhật ảnh đại diện";
            }
        } catch (e) {
            error = "Lỗi kết nối server";
        } finally {
            savingAvatar = false;
        }
    }

    async function handleFileUpload(e) {
        const file = e.target.files[0];
        if (!file) return;

        uploadingFile = true;
        error = "";
        successMsg = "";

        const formData = new FormData();
        formData.append("avatar", file);

        try {
            const response = await fetch(`${API_URL}/api/me/avatar/upload`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${$auth.token}`,
                },
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                successMsg = "Tải ảnh đại diện lên thành công!";
                userProfile.avatar_url = data.avatar_url;
                userProfile.avatar_seed = null;
                avatarSeed = ""; // Clear seed preview

                // Update auth store
                const updatedUser = {
                    ...$auth.user,
                    avatar_url: data.avatar_url,
                    avatar_seed: null,
                };
                auth.update((curr) => ({ ...curr, user: updatedUser }));

                setTimeout(() => (successMsg = ""), 3000);
            } else {
                const data = await response.json();
                error = data.msg || "Không thể tải ảnh lên";
            }
        } catch (e) {
            error = "Lỗi kết nối server";
        } finally {
            uploadingFile = false;
        }
    }

    function addLink() {
        linksList.push({ title: "Facebook", url: "", id: Math.random() });
    }

    function removeLink(index) {
        linksList.splice(index, 1);
        linksList = [...linksList]; // Trigger reactivity
    }

    async function saveProfileInfo() {
        if (savingProfile) return;
        savingProfile = true;
        error = "";
        successMsg = "";

        // Convert list to dict
        const social_links = {};
        for (const link of linksList) {
            if (link.title && link.url) {
                social_links[link.title] = link.url;
            }
        }

        try {
            const response = await fetch(`${API_URL}/api/me/profile`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${$auth.token}`,
                },
                body: JSON.stringify({
                    bio: bio,
                    social_links: social_links,
                }),
            });

            if (response.ok) {
                successMsg = "Cập nhật thông tin thành công!";
                userProfile.bio = bio;
                userProfile.social_links = social_links;
                setTimeout(() => (successMsg = ""), 3000);
            } else {
                error = "Không thể cập nhật thông tin";
            }
        } catch (e) {
            error = "Lỗi kết nối server";
        } finally {
            savingProfile = false;
        }
    }
</script>

<div class="max-w-[800px] mx-auto py-16 px-6">
    <header class="mb-12">
        <h1
            class="text-4xl font-extrabold text-fd-foreground tracking-tight mb-3"
        >
            Cài đặt tài khoản
        </h1>
        <p class="text-fd-muted font-medium text-sm">
            Quản lý thông tin cá nhân và tùy chỉnh hồ sơ của bạn.
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
            <!-- Profile Overview & Avatar Management -->
            <div class="fd-card overflow-hidden">
                <div
                    class="bg-fd-accent/30 p-8 flex flex-col md:flex-row items-center gap-10 border-b border-fd-border/50"
                >
                    <div class="relative group">
                        <div
                            role="button"
                            tabindex="0"
                            class="relative p-2 bg-white rounded-[2rem] shadow-2xl ring-1 ring-fd-border/50 group-hover:scale-105 transition-transform duration-500 cursor-pointer"
                            onclick={() => fileInput?.click()}
                            onkeydown={(e) => {
                                if (e.key === "Enter" || e.key === " ") {
                                    e.preventDefault();
                                    fileInput?.click();
                                }
                            }}
                        >
                            <Avatar
                                url={userProfile?.avatar_url}
                                seed={avatarSeed ||
                                    userProfile?.avatar_seed ||
                                    userProfile?.username}
                                size={120}
                                class="rounded-[1.5rem]"
                            />

                            <!-- Upload Button overlay -->
                            <div
                                class="absolute inset-2 bg-black/40 text-white opacity-0 group-hover:opacity-100 transition-opacity rounded-[1.5rem] flex flex-col items-center justify-center gap-1"
                            >
                                <i class="bx bx-camera text-2xl"></i>
                                <span
                                    class="text-[9px] font-bold uppercase tracking-widest"
                                    >Thay đổi</span
                                >
                            </div>

                            <!-- Randomize Shortcut Button -->
                            <button
                                onclick={(e) => {
                                    e.stopPropagation();
                                    randomizeAvatar();
                                }}
                                type="button"
                                class="absolute -bottom-2 -right-2 w-10 h-10 bg-fd-primary text-white rounded-full flex items-center justify-center shadow-lg hover:rotate-180 transition-all duration-500 border-4 border-white z-20"
                                title="Ngẫu nhiên"
                            >
                                <i class="bx bx-refresh text-xl"></i>
                            </button>
                        </div>
                        <input
                            type="file"
                            bind:this={fileInput}
                            onchange={handleFileUpload}
                            accept="image/*"
                            class="hidden"
                        />
                    </div>

                    <div class="flex-1 text-center md:text-left space-y-4">
                        <div class="space-y-1">
                            <h2
                                class="text-3xl font-black text-fd-foreground tracking-tighter"
                            >
                                {userProfile?.username}
                            </h2>
                            <p
                                class="text-fd-muted font-medium flex items-center gap-2 justify-center md:justify-start text-sm"
                            >
                                <i class="bx bx-envelope opacity-60"></i>
                                {userProfile?.email}
                            </p>
                        </div>

                        <div
                            class="flex flex-wrap items-center justify-center md:justify-start gap-4 pt-2"
                        >
                            <div
                                class="flex items-center gap-2 px-3 py-1.5 bg-fd-primary/10 rounded-full border border-fd-primary/20"
                            >
                                <div
                                    class="w-1.5 h-1.5 bg-fd-primary rounded-full animate-pulse"
                                ></div>
                                <span
                                    class="text-[10px] font-black uppercase tracking-widest text-fd-primary"
                                >
                                    {userProfile?.is_admin
                                        ? "Quản trị viên"
                                        : "Học viên"}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Avatar Customization Detail -->
                <div class="p-8 space-y-6 bg-fd-card/50">
                    <div class="flex flex-col md:flex-row md:items-end gap-6">
                        <div class="flex-1 space-y-2">
                            <label
                                for="avatar-seed"
                                class="text-xs font-black uppercase tracking-widest text-fd-muted ml-1"
                            >
                                Mã hạt giống (Avatar Seed)
                            </label>
                            <div class="relative">
                                <input
                                    id="avatar-seed"
                                    bind:value={avatarSeed}
                                    type="text"
                                    placeholder={userProfile?.avatar_url
                                        ? "Đang dùng ảnh tải lên..."
                                        : "Ví dụ: adventurous-soul..."}
                                    class="w-full bg-fd-background border border-fd-border rounded-xl px-4 py-3 text-sm font-bold focus:ring-2 focus:ring-fd-primary/20 focus:border-fd-primary transition-all outline-none"
                                />
                                <button
                                    onclick={randomizeAvatar}
                                    type="button"
                                    class="absolute right-3 top-1/2 -translate-y-1/2 text-fd-muted hover:text-fd-primary transition-colors"
                                    title="Ngẫu nhiên"
                                >
                                    <i class="bx bx-shuffle text-lg"></i>
                                </button>
                            </div>
                            <p
                                class="text-[10px] text-fd-muted font-medium ml-1"
                            >
                                Thay đổi mã này để tạo hình đại diện độc nhất
                                của bạn.
                            </p>
                        </div>
                        <button
                            onclick={saveAvatar}
                            disabled={savingAvatar ||
                                avatarSeed === userProfile?.avatar_seed}
                            class="px-8 py-3.5 bg-fd-primary text-white rounded-xl font-black text-xs uppercase tracking-[0.2em] shadow-[0_10px_20px_-10px_var(--primary-glow)] hover:-translate-y-0.5 active:translate-y-0 transition-all disabled:opacity-50 disabled:grayscale disabled:translate-y-0"
                        >
                            {#if savingAvatar}
                                <i class="bx bx-loader-alt animate-spin mr-2"
                                ></i> Đang lưu...
                            {:else}
                                Lưu thay đổi
                            {/if}
                        </button>
                    </div>

                    {#if successMsg}
                        <div
                            in:fade
                            class="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-500 text-center text-[11px] font-black uppercase tracking-widest"
                        >
                            <i class="bx bx-check-circle mr-1"></i>
                            {successMsg}
                        </div>
                    {/if}
                </div>
            </div>

            <!-- Profile Info Card -->
            <div class="fd-card p-8 space-y-6">
                <div class="flex items-center justify-between">
                    <h3
                        class="text-sm font-black uppercase tracking-widest text-fd-foreground flex items-center gap-3"
                    >
                        <div
                            class="w-8 h-8 rounded-lg bg-fd-primary/10 text-fd-primary flex items-center justify-center"
                        >
                            <i class="bx bx-id-card text-lg"></i>
                        </div>
                        Thông tin cá nhân
                    </h3>
                    <button
                        onclick={saveProfileInfo}
                        disabled={savingProfile}
                        class="px-4 py-1.5 bg-fd-primary text-white rounded-lg text-[10px] font-black uppercase tracking-widest shadow-lg hover:shadow-fd-primary/20 transition-all disabled:opacity-50"
                    >
                        {#if savingProfile}
                            <i class="bx bx-loader-alt animate-spin"></i>
                        {:else}
                            Lưu thông tin
                        {/if}
                    </button>
                </div>

                <div class="space-y-4">
                    <div class="space-y-2">
                        <label
                            for="bio"
                            class="text-xs font-black uppercase tracking-widest text-fd-muted ml-1"
                            >Giới thiệu (Bio)</label
                        >
                        <textarea
                            id="bio"
                            bind:value={bio}
                            rows="3"
                            placeholder="Một chút về bản thân bạn..."
                            class="w-full bg-fd-background border border-fd-border rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-fd-primary/20 focus:border-fd-primary transition-all outline-none resize-none"
                        ></textarea>
                    </div>

                    <div class="space-y-2">
                        <div class="flex items-center justify-between">
                            <label
                                class="text-xs font-black uppercase tracking-widest text-fd-muted ml-1"
                                >Liên kết xã hội</label
                            >
                            <button
                                onclick={addLink}
                                class="text-[10px] font-bold text-fd-primary hover:underline"
                                >+ Thêm liên kết</button
                            >
                        </div>

                        {#if linksList.length === 0}
                            <div
                                class="p-4 rounded-xl border border-dashed border-fd-border text-center"
                            >
                                <span class="text-xs text-fd-muted"
                                    >Chưa có liên kết nào</span
                                >
                            </div>
                        {:else}
                            <div class="space-y-2">
                                {#each linksList as link, i}
                                    <div class="flex gap-2">
                                        <input
                                            bind:value={link.title}
                                            placeholder="Tên (VD: Facebook)"
                                            class="w-1/3 bg-fd-background border border-fd-border rounded-lg px-3 py-2 text-xs font-bold focus:border-fd-primary outline-none"
                                        />
                                        <input
                                            bind:value={link.url}
                                            placeholder="URL (https://...)"
                                            class="flex-1 bg-fd-background border border-fd-border rounded-lg px-3 py-2 text-xs font-medium focus:border-fd-primary outline-none"
                                        />
                                        <button
                                            onclick={() => removeLink(i)}
                                            class="w-8 h-8 flex items-center justify-center text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
                                        >
                                            <i class="bx bx-trash"></i>
                                        </button>
                                    </div>
                                {/each}
                            </div>
                        {/if}
                    </div>
                </div>
            </div>

            <!-- Additional Info Sections -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Security Card -->
                <div class="fd-card p-8 space-y-6">
                    <h3
                        class="text-sm font-black uppercase tracking-widest text-fd-foreground flex items-center gap-3"
                    >
                        <div
                            class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-500 flex items-center justify-center"
                        >
                            <i class="bx bx-shield-quarter text-lg"></i>
                        </div>
                        Bảo mật tài khoản
                    </h3>
                    <div class="space-y-4">
                        <div
                            class="p-4 bg-fd-background/50 rounded-2xl border border-fd-border/50 group hover:border-fd-primary/30 transition-colors"
                        >
                            <p
                                class="text-[10px] text-fd-muted uppercase font-black tracking-widest mb-2 opacity-60"
                            >
                                Trạng thái bảo vệ
                            </p>
                            <div class="flex items-center gap-2">
                                <span class="text-xs font-bold text-emerald-500"
                                    >Đã kích hoạt 2FA</span
                                >
                                <i class="bx bxs-check-shield text-emerald-500"
                                ></i>
                            </div>
                        </div>
                        <button
                            class="w-full py-3 px-4 rounded-xl border border-fd-border text-[10px] font-black uppercase tracking-widest text-fd-muted hover:bg-fd-accent transition-all ring-1 ring-transparent hover:ring-fd-border"
                        >
                            Đổi mật khẩu
                        </button>
                    </div>
                </div>

                <!-- Stats Card -->
                <div class="fd-card p-8 space-y-6">
                    <h3
                        class="text-sm font-black uppercase tracking-widest text-fd-foreground flex items-center gap-3"
                    >
                        <div
                            class="w-8 h-8 rounded-lg bg-fd-primary/10 text-fd-primary flex items-center justify-center"
                        >
                            <i class="bx bx-bolt-circle text-lg"></i>
                        </div>
                        Thống kê học tập
                    </h3>
                    <div class="space-y-4">
                        <div
                            class="p-4 bg-fd-background/50 rounded-2xl border border-fd-border/50 group hover:border-fd-primary/30 transition-colors"
                        >
                            <p
                                class="text-[10px] text-fd-muted uppercase font-black tracking-widest mb-2 opacity-60"
                            >
                                ID Người dùng
                            </p>
                            <span
                                class="text-xs font-mono font-bold text-fd-muted"
                                >#{userProfile?.id
                                    ?.toString()
                                    .padStart(6, "0")}</span
                            >
                        </div>
                        <button
                            class="w-full py-3 px-4 rounded-xl bg-red-500/5 text-red-500 border border-red-500/10 text-[10px] font-black uppercase tracking-widest hover:bg-red-500 hover:text-white transition-all"
                        >
                            Vô hiệu hóa tài khoản
                        </button>
                    </div>
                </div>
            </div>
        {/if}

        {#if error}
            <div
                class="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-500 text-center text-xs font-bold"
            >
                {error}
            </div>
        {/if}
    </div>
</div>

<style>
    :global(.fd-card) {
        background: var(--fd-card);
        border: 1px solid var(--fd-border);
        border-radius: 1.5rem;
        box-shadow:
            0 4px 6px -1px rgb(0 0 0 / 0.1),
            0 2px 4px -2px rgb(0 0 0 / 0.1);
    }
</style>
