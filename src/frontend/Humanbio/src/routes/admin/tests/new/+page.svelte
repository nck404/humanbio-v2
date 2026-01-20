<script>
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import { fly, fade } from "svelte/transition";
    import { settings } from "$lib/stores/settings";
    import { API_URL } from "$lib/constants";

    let title = $state("");
    let description = $state("");
    let category = $state("General");
    let questions = $state([]);
    let loading = $state(false);
    let error = $state("");

    function addQuestion(type) {
        questions = [
            ...questions,
            {
                type,
                text: "",
                image_data: "",
                options:
                    type === "multiple_choice"
                        ? ["", "", "", ""]
                        : ["True", "False"],
                correct_answer: "",
                id: Date.now(),
            },
        ];
    }

    function removeQuestion(id) {
        questions = questions.filter((q) => q.id !== id);
    }

    async function handleImageUpload(e, index) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            questions[index].image_data = event.target.result;
        };
        reader.readAsDataURL(file);
    }

    async function saveTest() {
        if (!title || questions.length === 0) {
            error = "Vui lòng nhập tiêu đề và thêm ít nhất một câu hỏi";
            return;
        }

        loading = true;
        error = "";

        try {
            const res = await fetch(`${API_URL}/api/admin/tests`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${$auth.token}`,
                },
                body: JSON.stringify({
                    title,
                    description,
                    category,
                    questions,
                }),
            });

            if (res.ok) {
                goto("/admin");
            } else {
                const data = await res.json();
                error = data.msg || "Lưu đề thi thất bại";
            }
        } catch (e) {
            error = "Lỗi kết nối hệ thống";
        } finally {
            loading = false;
        }
    }
</script>

<div class="max-w-5xl mx-auto py-12 px-6">
    <div
        class="mb-12 flex flex-col md:flex-row justify-between items-start md:items-end gap-6"
    >
        <div>
            <div class="flex items-center gap-3 mb-4">
                <a
                    href="/admin"
                    class="w-10 h-10 rounded-2xl bg-fd-secondary border border-fd-border flex items-center justify-center text-fd-muted hover:text-fd-primary hover:border-fd-primary/50 transition-all"
                    aria-label="Back to admin"
                >
                    <i class="bx bx-left-arrow-alt text-2xl"></i>
                </a>
                <span class="fd-label mb-0">Trình biên soạn Đề thi</span>
            </div>
            <h1 class="text-5xl font-[900] text-fd-foreground tracking-tighter">
                Thiết kế Bài đánh giá
            </h1>
        </div>
        <button
            onclick={saveTest}
            disabled={loading}
            class="fd-btn-primary !px-10 !py-4 !rounded-[2rem] shadow-xl shadow-fd-primary/20 disabled:opacity-50"
        >
            {#if loading}
                <i class="bx bx-loader-alt animate-spin mr-2"></i>
            {/if}
            Công bố Đề thi
        </button>
    </div>

    <div class="space-y-10">
        <!-- Basic Info -->
        <div
            class="fd-card !p-8 !rounded-[2.5rem] border-fd-primary/10 shadow-2xl shadow-fd-primary/5"
        >
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
                <div class="md:col-span-1">
                    <label class="fd-label" for="test-title"
                        >Thông tin Cơ bản</label
                    >
                    <h2 class="text-xl font-black text-fd-foreground mb-2">
                        Định danh Bài thi
                    </h2>
                    <p class="text-fd-muted text-xs leading-relaxed">
                        Cung cấp tiêu đề và ngữ cảnh cụ thể cho bài đánh giá y
                        sinh của bạn.
                    </p>
                </div>
                <div class="md:col-span-2 space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label for="test-title" class="fd-label ml-1"
                                >Tiêu đề</label
                            >
                            <input
                                id="test-title"
                                bind:value={title}
                                type="text"
                                placeholder="VD: Hệ Tuần hoàn"
                                class="fd-input w-full !py-3 !rounded-2xl"
                            />
                        </div>
                        <div>
                            <label for="test-cat" class="fd-label ml-1"
                                >Danh mục / Phân loại</label
                            >
                            <input
                                id="test-cat"
                                bind:value={category}
                                type="text"
                                placeholder="VD: Tim mạch học"
                                class="fd-input w-full !py-3 !rounded-2xl"
                            />
                        </div>
                    </div>
                    <div>
                        <label for="test-desc" class="fd-label ml-1"
                            >Mô tả chi tiết</label
                        >
                        <textarea
                            id="test-desc"
                            bind:value={description}
                            placeholder="Giải thích ngắn gọn nội dung cốt lõi của bài thi này..."
                            class="fd-input w-full !py-3 !rounded-2xl h-24 resize-none"
                        ></textarea>
                    </div>
                </div>
            </div>
        </div>

        {#if error}
            <div
                class="p-4 bg-red-500/10 border border-red-500/20 rounded-2xl text-red-500 text-sm font-bold text-center"
                in:fade
            >
                <i class="bx bx-error-circle mr-2"></i>
                {error}
            </div>
        {/if}

        <!-- Questions List -->
        <div class="space-y-8">
            {#each questions as q, i (q.id)}
                <div
                    transition:fly={{ y: 30 }}
                    class="fd-card !p-8 !rounded-[2.5rem] relative overflow-hidden group"
                >
                    <!-- Type Indicator -->
                    <div class="absolute top-0 right-0 p-6">
                        <span
                            class="text-[10px] font-black uppercase tracking-[0.2em] px-3 py-1 rounded-full {q.type ===
                            'multiple_choice'
                                ? 'bg-fd-primary text-white'
                                : 'bg-emerald-500 text-white'} shadow-lg"
                        >
                            {q.type === "multiple_choice"
                                ? "Trắc nghiệm"
                                : "Đúng / Sai"}
                        </span>
                    </div>

                    <div class="flex items-center gap-4 mb-10">
                        <div
                            class="w-12 h-12 bg-fd-secondary border border-fd-border rounded-2xl flex items-center justify-center font-[900] text-fd-primary text-xl"
                        >
                            {i + 1}
                        </div>
                        <h3
                            class="text-2xl font-black text-fd-foreground tracking-tight"
                        >
                            Nội dung Câu hỏi
                        </h3>
                        <button
                            onclick={() => removeQuestion(q.id)}
                            class="ml-auto w-10 h-10 rounded-xl hover:bg-red-500/10 text-fd-muted hover:text-red-500 transition-all flex items-center justify-center"
                            aria-label="Remove question"
                        >
                            <i class="bx bx-trash text-xl"></i>
                        </button>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
                        <div class="space-y-6">
                            <div>
                                <label for="q-text-{q.id}" class="fd-label ml-1"
                                    >Câu hỏi</label
                                >
                                <textarea
                                    id="q-text-{q.id}"
                                    bind:value={q.text}
                                    placeholder="Đặt câu hỏi thảo luận về sinh học tại đây..."
                                    class="fd-input w-full !py-4 !rounded-2xl h-32 resize-none text-base"
                                ></textarea>
                            </div>

                            <div>
                                <label class="fd-label ml-1" for="file-{q.id}"
                                    >Hình ảnh minh họa</label
                                >
                                <div class="flex items-center gap-4">
                                    <input
                                        type="file"
                                        accept="image/*"
                                        onchange={(e) =>
                                            handleImageUpload(e, i)}
                                        class="hidden"
                                        id="file-{q.id}"
                                    />
                                    <label
                                        for="file-{q.id}"
                                        class="flex items-center gap-3 px-6 py-3 bg-fd-secondary hover:bg-fd-accent border border-fd-border rounded-2xl cursor-pointer transition-all font-bold text-sm text-fd-foreground"
                                    >
                                        <i
                                            class="bx bx-image-add text-xl text-fd-primary"
                                        ></i>
                                        {q.image_data
                                            ? "Thay đổi hình ảnh"
                                            : "Thêm minh họa"}
                                    </label>
                                    {#if q.image_data}
                                        <button
                                            onclick={() => (q.image_data = "")}
                                            class="text-red-500 font-bold text-xs hover:underline"
                                            >Gỡ bỏ</button
                                        >
                                    {/if}
                                </div>
                                {#if q.image_data}
                                    <div
                                        class="mt-6 rounded-[1.5rem] overflow-hidden border border-fd-border shadow-2xl relative aspect-video bg-black/20"
                                    >
                                        <img
                                            src={q.image_data}
                                            class="w-full h-full object-contain"
                                            alt="Visual aid"
                                        />
                                    </div>
                                {/if}
                            </div>
                        </div>

                        <div class="space-y-6">
                            {#if q.type === "multiple_choice"}
                                <label
                                    class="fd-label ml-1"
                                    for="q-opt-{q.id}-0"
                                    >Các phương án & Đáp án</label
                                >
                                <div class="space-y-3">
                                    {#each q.options as opt, optIdx}
                                        <div
                                            class="flex items-center gap-3 group/opt"
                                        >
                                            <div
                                                class="relative flex items-center"
                                            >
                                                <input
                                                    type="radio"
                                                    name="correct-{q.id}"
                                                    value={q.options[optIdx]}
                                                    bind:group={
                                                        q.correct_answer
                                                    }
                                                    class="peer absolute opacity-0 w-8 h-8 cursor-pointer z-10"
                                                />
                                                <div
                                                    class="w-8 h-8 rounded-xl border-2 border-fd-border peer-checked:border-fd-primary peer-checked:bg-fd-primary/10 flex items-center justify-center transition-all"
                                                >
                                                    <i
                                                        class="bx bx-check text-xl scale-0 peer-checked:scale-100 text-fd-primary transition-transform"
                                                    ></i>
                                                </div>
                                            </div>
                                            <input
                                                id="q-opt-{q.id}-{optIdx}"
                                                bind:value={q.options[optIdx]}
                                                placeholder="Lựa chọn {optIdx +
                                                    1}"
                                                class="fd-input flex-grow !rounded-xl !py-2.5 transition-all focus:ring-0 peer-checked:border-fd-primary/30"
                                            />
                                        </div>
                                    {/each}
                                </div>
                            {:else}
                                <label class="fd-label ml-1"
                                    >Đáp án Đúng/Sai</label
                                >
                                <div class="grid grid-cols-2 gap-4">
                                    <label
                                        class="flex flex-col items-center justify-center gap-3 p-8 rounded-[2rem] border-2 transition-all cursor-pointer {q.correct_answer ===
                                        'True'
                                            ? 'bg-fd-primary/10 border-fd-primary'
                                            : 'bg-fd-secondary/30 border-fd-border hover:border-fd-muted'}"
                                    >
                                        <input
                                            type="radio"
                                            value="True"
                                            bind:group={q.correct_answer}
                                            class="hidden"
                                        />
                                        <div
                                            class="w-12 h-12 rounded-2xl flex items-center justify-center {q.correct_answer ===
                                            'True'
                                                ? 'bg-fd-primary text-white shadow-lg shadow-fd-primary/30'
                                                : 'bg-fd-card text-fd-muted'} transition-all"
                                        >
                                            <i class="bx bx-check text-2xl"></i>
                                        </div>
                                        <span
                                            class="font-black text-sm uppercase tracking-widest"
                                            >Đúng</span
                                        >
                                    </label>
                                    <label
                                        class="flex flex-col items-center justify-center gap-3 p-8 rounded-[2rem] border-2 transition-all cursor-pointer {q.correct_answer ===
                                        'False'
                                            ? 'bg-emerald-500/10 border-emerald-500'
                                            : 'bg-fd-secondary/30 border-fd-border hover:border-fd-muted'}"
                                    >
                                        <input
                                            type="radio"
                                            value="False"
                                            bind:group={q.correct_answer}
                                            class="hidden"
                                        />
                                        <div
                                            class="w-12 h-12 rounded-2xl flex items-center justify-center {q.correct_answer ===
                                            'False'
                                                ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30'
                                                : 'bg-fd-card text-fd-muted'} transition-all"
                                        >
                                            <i class="bx bx-x text-2xl"></i>
                                        </div>
                                        <span
                                            class="font-black text-sm uppercase tracking-widest"
                                            >Sai</span
                                        >
                                    </label>
                                </div>
                            {/if}
                        </div>
                    </div>
                </div>
            {/each}
        </div>

        <!-- Action Selection -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <button
                onclick={() => addQuestion("multiple_choice")}
                class="fd-card !p-10 !rounded-[2.5rem] border-dashed border-2 border-fd-border hover:border-fd-primary hover:bg-fd-primary/5 text-fd-muted hover:text-fd-primary transition-all flex flex-col items-center justify-center gap-4 group"
            >
                <div
                    class="w-16 h-16 rounded-3xl bg-fd-secondary group-hover:bg-fd-primary group-hover:text-white flex items-center justify-center transition-all"
                >
                    <i class="bx bx-list-ol text-4xl"></i>
                </div>
                <div class="text-center">
                    <span
                        class="block font-[900] text-xl text-fd-foreground group-hover:text-fd-primary transition-colors"
                        >Trắc nghiệm nhiều lựa chọn</span
                    >
                    <span
                        class="text-xs font-bold uppercase tracking-widest opacity-60"
                        >Thêm câu hỏi trắc nghiệm</span
                    >
                </div>
            </button>

            <button
                onclick={() => addQuestion("true_false")}
                class="fd-card !p-10 !rounded-[2.5rem] border-dashed border-2 border-fd-border hover:border-emerald-500 hover:bg-emerald-500/5 text-fd-muted hover:text-emerald-500 transition-all flex flex-col items-center justify-center gap-4 group"
            >
                <div
                    class="w-16 h-16 rounded-3xl bg-fd-secondary group-hover:bg-emerald-500 group-hover:text-white flex items-center justify-center transition-all"
                >
                    <i class="bx bx-check-double text-4xl"></i>
                </div>
                <div class="text-center">
                    <span
                        class="block font-[900] text-xl text-fd-foreground group-hover:text-emerald-500 transition-colors"
                        >Đúng / Sai</span
                    >
                    <span
                        class="text-xs font-bold uppercase tracking-widest opacity-60"
                        >Thêm câu hỏi nhị phân</span
                    >
                </div>
            </button>
        </div>
    </div>
</div>
