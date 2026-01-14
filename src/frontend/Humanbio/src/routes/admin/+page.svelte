<script>
    import { onMount } from "svelte";
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import { API_URL } from "$lib/constants";

    let stats = {
        tests: 0,
        users: 0,
        admins: 0,
    };
    let loading = true;
    let tests = [];
    let users = [];

    onMount(async () => {
        await loadData();
    });

    async function loadData() {
        loading = true;
        try {
            console.log(
                "Fetching admin data with token:",
                $auth.token?.substring(0, 10) + "...",
            );
            const [testsRes, usersRes] = await Promise.all([
                fetch(`${API_URL}/api/admin/tests`, {
                    headers: { Authorization: `Bearer ${$auth.token}` },
                }),
                fetch(`${API_URL}/api/admin/users`, {
                    headers: { Authorization: `Bearer ${$auth.token}` },
                }),
            ]);

            console.log("Tests response status:", testsRes.status);
            console.log("Users response status:", usersRes.status);

            if (testsRes.ok && usersRes.ok) {
                tests = await testsRes.json();
                users = await usersRes.json();

                stats = {
                    tests: tests.length,
                    users: users.length,
                    admins: users.filter((u) => u.is_admin).length,
                };
            } else {
                const testsErr = !testsRes.ok ? await testsRes.text() : "";
                const usersErr = !usersRes.ok ? await usersRes.text() : "";
                console.error(
                    "Failed to fetch. Tests:",
                    testsErr,
                    "Users:",
                    usersErr,
                );
                alert(
                    `Failed to load data. Tests: ${testsRes.status}, Users: ${usersRes.status}`,
                );
            }
        } catch (e) {
            console.error("Failed to load admin data", e);
            alert("Connection error while fetching admin data.");
        } finally {
            loading = false;
        }
    }

    async function deleteTest(id) {
        if (!confirm("Are you sure you want to delete this test?")) return;

        try {
            const res = await fetch(`${API_URL}/api/admin/tests/${id}`, {
                method: "DELETE",
                headers: { Authorization: `Bearer ${$auth.token}` },
            });
            if (res.ok) await loadData();
        } catch (e) {
            alert("Delete failed");
        }
    }

    async function promoteUser(id) {
        try {
            const res = await fetch(
                `${API_URL}/api/admin/users/${id}/promote`,
                {
                    method: "POST",
                    headers: { Authorization: `Bearer ${$auth.token}` },
                },
            );
            if (res.ok) await loadData();
        } catch (e) {
            alert("Promotion failed");
        }
    }
</script>

<div class="max-w-[1400px] mx-auto py-12 px-6">
    <div
        class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12"
    >
        <div in:fade={{ duration: 600 }}>
            <h1 class="text-6xl font-black text-fd-foreground tracking-tighter">
                Console<span class="text-fd-primary">.</span>
            </h1>
            <p
                class="text-fd-muted mt-2 font-bold text-xs uppercase tracking-widest opacity-80"
            >
                System Intelligence Hub
            </p>
        </div>
        <a
            href="/admin/tests/new"
            class="fd-btn-primary !px-8 !py-4 !rounded-xl group"
        >
            <i
                class="bx bx-plus text-xl group-hover:rotate-90 transition-transform"
            ></i>
            <span>Register New Test</span>
        </a>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
        <div
            class="fd-card !p-8 flex items-center gap-6 !rounded-[2rem] border-fd-primary/10 hover:border-fd-primary transition-all duration-500"
        >
            <div
                class="w-14 h-14 bg-fd-primary/10 text-fd-primary rounded-2xl flex items-center justify-center shadow-inner"
            >
                <i class="bx bx-atom text-3xl"></i>
            </div>
            <div>
                <p class="fd-label !mb-0 text-fd-primary">Biological Units</p>
                <p
                    class="text-4xl font-black text-fd-foreground tracking-tighter"
                >
                    {stats.tests.toString().padStart(2, "0")}
                </p>
            </div>
        </div>
        <div
            class="fd-card !p-8 flex items-center gap-6 !rounded-[2rem] border-emerald-500/10 hover:border-emerald-500 transition-all duration-500"
        >
            <div
                class="w-14 h-14 bg-emerald-500/10 text-emerald-500 rounded-2xl flex items-center justify-center shadow-inner"
            >
                <i class="bx bxs-group text-3xl"></i>
            </div>
            <div>
                <p class="fd-label !mb-0 text-emerald-500">User Network</p>
                <p
                    class="text-4xl font-black text-fd-foreground tracking-tighter"
                >
                    {stats.users.toString().padStart(2, "0")}
                </p>
            </div>
        </div>
        <div
            class="fd-card !p-8 flex items-center gap-6 !rounded-[2rem] border-amber-500/10 hover:border-amber-500 transition-all duration-500"
        >
            <div
                class="w-14 h-14 bg-amber-500/10 text-amber-500 rounded-2xl flex items-center justify-center shadow-inner"
            >
                <i class="bx bxs-shield-alt-2 text-3xl"></i>
            </div>
            <div>
                <p class="fd-label !mb-0 text-amber-500">Verified Access</p>
                <p
                    class="text-4xl font-black text-fd-foreground tracking-tighter"
                >
                    {stats.admins.toString().padStart(2, "0")}
                </p>
            </div>
        </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Mock Tests Section -->
        <section class="space-y-6">
            <div class="flex items-center justify-between px-2">
                <span
                    class="fd-label mb-0 flex items-center gap-2 text-fd-foreground"
                >
                    <i class="bx bx-dna text-fd-primary text-lg"></i>
                    Library Genesis
                </span>
                <span class="text-[10px] font-bold text-fd-muted"
                    >{stats.tests} TOTAL</span
                >
            </div>
            <div
                class="fd-card !p-2 overflow-hidden !rounded-[2rem] bg-fd-secondary/30"
            >
                <div class="flex flex-col gap-1.5">
                    {#if loading}
                        <div class="p-16 text-center">
                            <i
                                class="bx bx-loader-alt animate-spin text-3xl text-fd-primary opacity-50"
                            ></i>
                        </div>
                    {:else if tests.length === 0}
                        <div
                            class="p-16 text-center text-fd-muted text-sm font-medium"
                        >
                            No modules found.
                        </div>
                    {:else}
                        {#each tests as test}
                            <div
                                class="p-4 bg-white border border-fd-border/50 rounded-2xl flex justify-between items-center hover:border-fd-primary/30 hover:shadow-lg transition-all group"
                            >
                                <div class="flex items-center gap-4">
                                    <div
                                        class="w-11 h-11 bg-fd-primary/5 rounded-xl flex items-center justify-center text-fd-primary group-hover:scale-110 transition-transform"
                                    >
                                        <i class="bx bxs-file-blank text-xl"
                                        ></i>
                                    </div>
                                    <div>
                                        <h3
                                            class="font-black text-fd-foreground text-sm"
                                        >
                                            {test.title}
                                        </h3>
                                        <div
                                            class="flex items-center gap-2 mt-0.5"
                                        >
                                            <span
                                                class="fd-badge fd-badge-primary !px-2 !py-0.5 !text-[8px] !bg-fd-primary/10 !text-fd-primary !border-none"
                                            >
                                                <i class="bx bxs-folder mr-1"
                                                ></i>{test.category ||
                                                    "General"}
                                            </span>
                                            <span
                                                class="fd-badge fd-badge-primary !px-2 !py-0.5 !text-[8px]"
                                                >{test.question_count} Units</span
                                            >
                                        </div>
                                    </div>
                                </div>
                                <div class="flex gap-1">
                                    <a
                                        href="/admin/tests/{test.id}"
                                        class="p-2 text-fd-muted hover:text-fd-primary hover:bg-fd-primary/10 rounded-xl transition-all"
                                        aria-label="Edit test"
                                    >
                                        <i class="bx bx-edit-alt text-lg"></i>
                                    </a>
                                    <button
                                        onclick={() => deleteTest(test.id)}
                                        class="p-2 text-fd-muted hover:text-red-500 hover:bg-red-500/10 rounded-xl transition-all"
                                        aria-label="Delete test"
                                    >
                                        <i class="bx bx-trash text-lg"></i>
                                    </button>
                                </div>
                            </div>
                        {/each}
                    {/if}
                </div>
            </div>
        </section>

        <!-- Users Section -->
        <section class="space-y-6">
            <div class="flex items-center justify-between px-2">
                <span
                    class="fd-label mb-0 flex items-center gap-2 text-fd-foreground"
                >
                    <i class="bx bxs-user-detail text-emerald-500 text-lg"></i>
                    Personnel Registry
                </span>
                <span class="text-[10px] font-bold text-fd-muted"
                    >{stats.users} ENROLLED</span
                >
            </div>
            <div
                class="fd-card !p-2 overflow-hidden !rounded-[2rem] bg-fd-secondary/30"
            >
                <div
                    class="flex flex-col gap-1.5 max-h-[600px] overflow-y-auto pr-1"
                >
                    {#if loading}
                        <div
                            class="p-16 text-center text-fd-primary opacity-50"
                        >
                            <i class="bx bx-loader-alt animate-spin text-3xl"
                            ></i>
                        </div>
                    {:else}
                        {#each users as user}
                            <div
                                class="p-4 bg-white border border-fd-border/50 rounded-2xl flex justify-between items-center hover:border-emerald-500/30 transition-all group"
                            >
                                <div class="flex items-center gap-4">
                                    <div
                                        class="w-12 h-12 rounded-xl bg-fd-accent border border-fd-border flex items-center justify-center text-xs text-fd-primary font-black shadow-sm group-hover:scale-110 transition-transform"
                                    >
                                        {user.username
                                            .substring(0, 2)
                                            .toUpperCase()}
                                    </div>
                                    <div>
                                        <h3
                                            class="font-black text-fd-foreground text-sm flex items-center gap-2"
                                        >
                                            {user.username}
                                            {#if user.is_admin}
                                                <span
                                                    class="fd-badge fd-badge-primary !bg-fd-primary !text-white !text-[8px]"
                                                    >Auth: Root</span
                                                >
                                            {/if}
                                        </h3>
                                        <p
                                            class="text-[11px] text-fd-muted font-bold tracking-tight opacity-70"
                                        >
                                            {user.email}
                                        </p>
                                    </div>
                                </div>
                                {#if !user.is_admin}
                                    <button
                                        onclick={() => promoteUser(user.id)}
                                        class="fd-btn-ghost !text-[9px] !px-4 !py-2 !rounded-xl !border-fd-border hover:!border-fd-primary font-black uppercase tracking-widest transition-all"
                                    >
                                        Elevate
                                    </button>
                                {/if}
                            </div>
                        {/each}
                    {/if}
                </div>
            </div>
        </section>
    </div>
</div>
