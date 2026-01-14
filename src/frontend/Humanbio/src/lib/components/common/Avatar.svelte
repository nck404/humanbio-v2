<script>
    let { seed = "default", size = 40, class: className = "" } = $props();

    let avatarUrl = $derived(
        `https://api.dicebear.com/7.x/avataaars/svg?seed=${seed}&backgroundColor=b6e3f4,c0aede,d1d4f9`,
    );
</script>

<div
    class="relative overflow-hidden shrink-0 {className}"
    style:width="{size}px"
    style:height="{size}px"
>
    <img
        src={avatarUrl}
        alt="User Avatar"
        class="w-full h-full object-cover"
        loading="lazy"
    />
</div>
