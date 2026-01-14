<script>
    import { createEventDispatcher } from "svelte";
    import { anatomyData } from "$lib/data/anatomy";
    import { fly, fade } from "svelte/transition";

    const dispatch = createEventDispatcher();
    let hoveredPart = null;

    function handleSelect(part) {
        dispatch("select", part);
    }
</script>

<div
    class="relative w-full max-w-[500px] h-[600px] mx-auto select-none rounded-[2rem] overflow-hidden shadow-2xl bg-black"
>
    <!-- Realistic Base Image -->
    <img
        src="/anatomy_base.png"
        alt="Human Anatomy"
        class="absolute inset-0 w-full h-full object-cover"
    />

    <!-- Cinematic Overlay to ensure text readability if needed -->
    <div
        class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-black/10 pointer-events-none"
    ></div>

    <!-- SVG Interaction Layer -->
    <svg viewBox="0 0 500 600" class="absolute inset-0 w-full h-full z-10">
        {#each anatomyData as part}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <g
                role="button"
                tabindex="0"
                on:click={() => handleSelect(part)}
                on:keydown={(e) =>
                    (e.key === "Enter" || e.key === " ") && handleSelect(part)}
                on:mouseenter={() => (hoveredPart = part.id)}
                on:mouseleave={() => (hoveredPart = null)}
                on:focus={() => (hoveredPart = part.id)}
                on:blur={() => (hoveredPart = null)}
                class="cursor-pointer group focus:outline-none"
            >
                <!-- Path acts as hit area, invisible until hovered -->
                <path
                    d={part.path}
                    fill={hoveredPart === part.id ? part.color : "transparent"}
                    fill-opacity={hoveredPart === part.id ? 0.3 : 0}
                    stroke={hoveredPart === part.id
                        ? part.color
                        : "transparent"}
                    stroke-width="3"
                    class="transition-all duration-300 filter drop-shadow-[0_0_5px_rgba(255,255,255,0.3)]"
                />

                <!-- Dynamic Label Line -->
                {#if hoveredPart === part.id}
                    <!-- Simple highlight dot instead of line to be cleaner over image -->
                    <circle
                        cx="250"
                        cy="100"
                        r="0"
                        fill="none"
                        class="hidden"
                    />
                {/if}
            </g>
        {/each}
    </svg>

    <!-- Floating Labels -->
    {#each anatomyData as part}
        {#if hoveredPart === part.id}
            <!-- Positioned Tooltip -->
            <div
                class="absolute bottom-8 left-1/2 -translate-x-1/2 bg-black/80 backdrop-blur-md border border-white/20 px-6 py-3 rounded-2xl text-center shadow-2xl pointer-events-none z-20"
                in:fly={{ y: 10, duration: 200 }}
            >
                <span
                    class="text-[10px] font-black uppercase tracking-widest text-fd-primary block mb-1"
                    >Đang chọn</span
                >
                <span class="text-xl font-bold text-white tracking-tight"
                    >{part.name}</span
                >
            </div>
        {/if}
    {/each}
</div>
