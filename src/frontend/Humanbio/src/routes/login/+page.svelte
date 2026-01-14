<script>
    import { onMount } from "svelte";
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import { fade, fly } from "svelte/transition";
    import { settings } from "$lib/stores/settings";
    import { API_URL } from "$lib/constants";

    let email = $state("");
    let password = $state("");
    let error = $state("");
    let loading = $state(false);
    let recaptchaToken = $state("");

    onMount(() => {
        // @ts-ignore
        if (window.grecaptcha) {
            // @ts-ignore
            window.grecaptcha.render("recaptcha-container", {
                sitekey: "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI",
                callback: (token) => {
                    recaptchaToken = token;
                },
            });
        }
    });

    async function handleLogin() {
        if (!recaptchaToken) {
            error = "Vui lòng hoàn thành xác nhận reCAPTCHA";
            return;
        }

        loading = true;
        error = "";

        try {
            const response = await fetch(`${API_URL}/api/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email,
                    password,
                    recaptcha_token: recaptchaToken,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                auth.set({
                    token: data.access_token,
                    user: data.user,
                    isAuthenticated: true,
                });

                // Initialize settings from user data
                if (data.user.settings) {
                    settings.set({
                        ...data.user.settings,
                        theme: "light", // Force light mode
                    });
                }

                goto("/");
            } else {
                error = data.msg || "Đăng nhập thất bại";
                // @ts-ignore
                window.grecaptcha.reset();
                recaptchaToken = "";
            }
        } catch (e) {
            error = "Đã xảy ra lỗi. Vui lòng thử lại.";
        } finally {
            loading = false;
        }
    }
</script>

<div
    class="min-h-[calc(100vh-2.75rem)] flex items-center justify-center py-12 px-6 relative overflow-hidden mesh-gradient"
>
    <!-- Dynamic Glows -->
    <div
        class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full blur-[140px] opacity-20 pointer-events-none"
        style="background: radial-gradient(circle, var(--primary), transparent)"
    ></div>

    <div
        class="max-w-md w-full relative z-10"
        in:fly={{ y: 20, duration: 800 }}
    >
        <div
            class="fd-card !p-10 !rounded-[3rem] shadow-2xl bg-fd-card/80 backdrop-blur-xl border-fd-primary/10"
        >
            <div class="text-center mb-12">
                <div
                    class="inline-flex items-center justify-center w-16 h-16 rounded-[1.5rem] bg-fd-primary text-white mb-6 shadow-2xl shadow-fd-primary/30"
                >
                    <i class="bx bx-lock-open text-3xl"></i>
                </div>
                <h2
                    class="text-4xl font-[900] text-fd-foreground tracking-tighter"
                >
                    Xác thực
                </h2>
                <p
                    class="mt-3 text-sm text-fd-muted font-bold tracking-tight opacity-70"
                >
                    Cổng truy cập hệ thống Human Biology
                </p>
            </div>

            <form
                class="space-y-8"
                onsubmit={(e) => {
                    e.preventDefault();
                    handleLogin();
                }}
            >
                <div class="space-y-5">
                    <div class="space-y-2">
                        <label for="email-address" class="fd-label ml-1"
                            >ID Truy cập</label
                        >
                        <div class="relative group">
                            <div
                                class="absolute inset-y-0 left-4 flex items-center pointer-events-none text-fd-muted group-focus-within:text-fd-primary transition-colors"
                            >
                                <i class="bx bx-dna text-xl"></i>
                            </div>
                            <input
                                id="email-address"
                                type="email"
                                required
                                class="fd-input w-full !pl-12 !py-4 !rounded-2xl !bg-fd-secondary/30"
                                placeholder="name@network.com"
                                bind:value={email}
                            />
                        </div>
                    </div>

                    <div class="space-y-2">
                        <div class="flex items-center justify-between ml-1">
                            <label for="password" class="fd-label mb-0"
                                >Mã bảo mật</label
                            >
                            <a
                                href="/forgot"
                                class="text-[10px] font-black uppercase tracking-widest text-fd-primary hover:underline"
                                >Quên mã?</a
                            >
                        </div>
                        <div class="relative group">
                            <div
                                class="absolute inset-y-0 left-4 flex items-center pointer-events-none text-fd-muted group-focus-within:text-fd-primary transition-colors"
                            >
                                <i class="bx bx-shield-quarter text-xl"></i>
                            </div>
                            <input
                                id="password"
                                type="password"
                                required
                                class="fd-input w-full !pl-12 !py-4 !rounded-2xl !bg-fd-secondary/30"
                                placeholder="••••••••"
                                bind:value={password}
                            />
                        </div>
                    </div>
                </div>

                <div
                    class="flex justify-center transform scale-90 origin-center py-2"
                >
                    <div
                        id="recaptcha-container"
                        class="rounded-xl overflow-hidden border border-fd-border/50"
                    ></div>
                </div>

                {#if error}
                    <div
                        class="text-red-500 text-xs font-black uppercase tracking-widest px-4 py-3 rounded-2xl bg-red-500/10 border border-red-500/20 text-center"
                    >
                        <i class="bx bx-error-circle mr-2"></i>
                        {error}
                    </div>
                {/if}

                <button
                    type="submit"
                    disabled={loading}
                    class="fd-btn-primary w-full !py-4.5 !rounded-2xl group relative overflow-hidden"
                >
                    <span class="relative z-10 flex items-center gap-3">
                        {#if loading}
                            <i class="bx bx-loader-alt animate-spin text-xl"
                            ></i>
                            Đang xử lý...
                        {:else}
                            Xác thực & Truy cập
                            <i
                                class="bx bx-right-arrow-alt text-2xl group-hover:translate-x-2 transition-transform"
                            ></i>
                        {/if}
                    </span>
                    <div
                        class="absolute inset-0 bg-white/10 translate-y-full group-hover:translate-y-0 transition-transform duration-300"
                    ></div>
                </button>
            </form>

            <div class="mt-10 pt-10 border-t border-fd-border/50 text-center">
                <p class="text-xs text-fd-muted font-bold tracking-tight">
                    Chưa có tài khoản?
                    <a
                        href="/register"
                        class="text-fd-foreground hover:text-fd-primary transition-colors font-black border-b border-fd-primary"
                    >
                        Đăng ký thành viên
                    </a>
                </p>
            </div>
        </div>
    </div>
</div>
