<script>
    import { onMount } from "svelte";
    import { fade, fly, slide } from "svelte/transition";
    import { settings } from "$lib/stores/settings";
    import { API_URL } from "$lib/constants";

    let tests = $state([]);
    let searchQuery = $state("");
    let loading = $state(true);
    let expandedFolders = $state(new Set());

    onMount(async () => {
        await fetchTests();
    });

    async function fetchTests() {
        loading = true;
        try {
            const res = await fetch(`${API_URL}/api/tests?q=${searchQuery}`);
            if (res.ok) {
                const data = await res.json();
                tests = data;
                // Auto-expand all folders initially
                const categories = [...new Set(data.map((t) => t.category))];
                expandedFolders = new Set(categories);
            }
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }

    let filteredTests = $derived(
        tests.filter(
            (t) =>
                t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                t.category.toLowerCase().includes(searchQuery.toLowerCase()),
        ),
    );

    let groupedTests = $derived(
        filteredTests.reduce((acc, test) => {
            if (!acc[test.category]) acc[test.category] = [];
            acc[test.category].push(test);
            return acc;
        }, {}),
    );

    function toggleFolder(category) {
        if (expandedFolders.has(category)) {
            expandedFolders.delete(category);
        } else {
            expandedFolders.add(category);
        }
        expandedFolders = new Set(expandedFolders);
    }
</script>

<div class="max-w-7xl mx-auto py-16 px-6">
    <!-- Header Section -->
    <div
        class="mb-16 flex flex-col md:flex-row justify-between items-start md:items-end gap-8"
    >
        <div class="space-y-4">
            <div class="flex items-center gap-3">
                <span class="fd-badge bg-fd-primary/10 text-fd-primary"
                    >Clinical Hub</span
                >
                <span
                    class="text-[10px] font-black text-fd-muted uppercase tracking-[0.3em] opacity-40"
                    >Examination Core</span
                >
            </div>
            <h1
                class="text-6xl font-[1000] text-fd-foreground tracking-tighter leading-none"
            >
                Medical <br /><span class="text-fd-primary italic"
                    >Assessments</span
                >
            </h1>
            <p
                class="text-fd-muted font-medium max-w-md text-base leading-relaxed"
            >
                Validate your clinical knowledge with our curated mock tests.
                Grouped by biological systems.
            </p>
        </div>

        <div class="relative w-full max-w-md group">
            <i
                class="bx bx-search absolute left-5 top-1/2 -translate-y-1/2 text-fd-primary text-xl transition-transform group-focus-within:scale-120"
            ></i>
            <input
                type="text"
                bind:value={searchQuery}
                oninput={fetchTests}
                placeholder="Search by system or topic..."
                class="w-full bg-fd-secondary/30 border border-fd-border rounded-[2rem] pl-14 pr-6 py-4 text-fd-foreground font-black placeholder:text-fd-muted/50 focus:ring-4 focus:ring-fd-primary/10 focus:border-fd-primary transition-all outline-none"
            />
        </div>
    </div>

    {#if loading}
        <div class="flex flex-col items-center justify-center py-32 gap-6">
            <div
                class="w-16 h-16 border-4 border-fd-primary/10 border-t-fd-primary rounded-full animate-spin shadow-xl"
            ></div>
            <p
                class="text-[10px] font-black uppercase tracking-[0.5em] text-fd-primary animate-pulse"
            >
                Syncing Test Repositories
            </p>
        </div>
    {:else if Object.keys(groupedTests).length === 0}
        <div
            class="text-center py-40 bg-fd-secondary/10 rounded-[4rem] border-2 border-dashed border-fd-border"
        >
            <i class="bx bx-folder-open text-7xl text-fd-muted opacity-20 mb-6"
            ></i>
            <p
                class="text-xl font-black text-fd-muted uppercase tracking-widest"
            >
                No diagnostics found
            </p>
            <button
                onclick={() => (searchQuery = "")}
                class="mt-4 text-fd-primary font-bold hover:underline"
                >Clear search filters</button
            >
        </div>
    {:else}
        <div class="space-y-12">
            {#each Object.entries(groupedTests) as [category, categoryTests]}
                <div class="space-y-6">
                    <!-- Folder Header -->
                    <button
                        onclick={() => toggleFolder(category)}
                        class="flex items-center gap-4 w-full text-left group"
                        aria-expanded={expandedFolders.has(category)}
                    >
                        <div
                            class="w-10 h-10 rounded-xl bg-fd-primary/10 flex items-center justify-center text-fd-primary transition-all {expandedFolders.has(
                                category,
                            )
                                ? 'rotate-0 shadow-lg'
                                : '-rotate-90 opacity-50'}"
                        >
                            <i class="bx bxs-folder text-2xl"></i>
                        </div>
                        <h2
                            class="text-2xl font-black text-fd-foreground tracking-tight flex-1"
                        >
                            {category}
                            <span
                                class="ml-2 text-[10px] text-fd-muted font-bold px-2 py-0.5 bg-fd-secondary rounded-md uppercase tracking-widest leading-none align-middle"
                            >
                                {categoryTests.length} Items
                            </span>
                        </h2>
                        <div
                            class="h-px flex-1 bg-fd-border/30 mx-4 hidden sm:block"
                        ></div>
                        <i
                            class="bx {expandedFolders.has(category)
                                ? 'bx-chevron-up'
                                : 'bx-chevron-down'} text-fd-muted text-2xl group-hover:text-fd-primary transition-colors"
                        ></i>
                    </button>

                    <!-- Folder Content -->
                    {#if expandedFolders.has(category)}
                        <div
                            transition:slide
                            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
                        >
                            {#each categoryTests as test (test.id)}
                                <a
                                    href="/tests/{test.id}"
                                    class="fd-card group !p-0 overflow-hidden !rounded-[2.5rem] border-fd-border/40 hover:border-fd-primary/40 hover:shadow-2xl hover:shadow-fd-primary/5 transition-all duration-500 hover:-translate-y-2 relative"
                                    in:fly={{
                                        y: 20,
                                        duration: 400 + (test.id % 5) * 100,
                                    }}
                                >
                                    <!-- Badge -->
                                    <div class="absolute top-6 right-6 z-10">
                                        <div
                                            class="bg-fd-background/50 backdrop-blur-md border border-fd-white/10 px-3 py-1 rounded-full flex items-center gap-1.5 shadow-sm"
                                        >
                                            <div
                                                class="w-1.5 h-1.5 rounded-full bg-fd-primary animate-pulse"
                                            ></div>
                                            <span
                                                class="text-[9px] font-black text-fd-foreground uppercase tracking-widest"
                                                >{test.question_count} Units</span
                                            >
                                        </div>
                                    </div>

                                    <!-- Card Content -->
                                    <div class="p-8 pt-10 flex flex-col h-full">
                                        <div
                                            class="w-14 h-14 rounded-2xl bg-fd-primary/5 border border-fd-primary/10 flex items-center justify-center mb-6 group-hover:bg-fd-primary group-hover:text-white transition-all duration-500"
                                        >
                                            <i class="bx bxs-layer text-3xl"
                                            ></i>
                                        </div>

                                        <h3
                                            class="text-2xl font-black text-fd-foreground group-hover:text-fd-primary transition-colors mb-3 leading-tight"
                                        >
                                            {test.title}
                                        </h3>

                                        <p
                                            class="text-[13px] text-fd-muted font-medium mb-8 flex-1 line-clamp-2 leading-relaxed"
                                        >
                                            {test.description ||
                                                "In-depth medical evaluation focusing on biological systems and clinical reasoning."}
                                        </p>

                                        <div
                                            class="flex items-center justify-between pt-6 border-t border-fd-border/20"
                                        >
                                            <div
                                                class="flex items-center gap-3"
                                            >
                                                <div
                                                    class="w-8 h-8 rounded-full bg-fd-accent flex items-center justify-center"
                                                >
                                                    <i
                                                        class="bx bx-time-five text-fd-muted text-sm"
                                                    ></i>
                                                </div>
                                                <span
                                                    class="text-[10px] font-black text-fd-muted uppercase tracking-wider"
                                                    >Practice Mode</span
                                                >
                                            </div>
                                            <div
                                                class="flex items-center gap-1 text-fd-primary font-black text-[11px] uppercase tracking-widest group-hover:translate-x-1 transition-transform"
                                            >
                                                Start <i
                                                    class="bx bx-right-arrow-alt text-xl"
                                                ></i>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Decorative Mesh -->
                                    <div
                                        class="absolute -bottom-10 -right-10 w-24 h-24 bg-fd-primary/10 blur-3xl rounded-full group-hover:scale-150 transition-transform duration-700"
                                    ></div>
                                </a>
                            {/each}
                        </div>
                    {/if}
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    @reference "../layout.css";
    .fd-badge {
        @apply px-3 py-1 rounded-md text-[9px] font-black uppercase tracking-[0.2em];
    }
</style>
