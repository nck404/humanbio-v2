<script>
    import { API_URL } from "$lib/constants";
    let {
        seed = "default",
        url = null,
        size = 40,
        class: className = "",
    } = $props();

    let avatarUrl = $derived(
        url
            ? url.startsWith("http")
                ? url
                : `${API_URL}${url}`
            : `https://api.dicebear.com/7.x/avataaars/svg?seed=${seed}&backgroundColor=b6e3f4,c0aede,d1d4f9`,
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
