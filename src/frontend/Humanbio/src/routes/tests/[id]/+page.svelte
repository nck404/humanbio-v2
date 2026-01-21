<script>
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { fade, fly, scale, slide } from "svelte/transition";
    import { settings } from "$lib/stores/settings";
    import { API_URL } from "$lib/constants";

    const testId = $page.params.id;
    let test = $state(null);
    let loading = $state(true);
    let currentQuestionIdx = $state(0);
    let userAnswers = $state({}); // { questionId: answer }
    let showResults = $state(false);
    let startTime = $state(Date.now());
    let endTime = $state(null);

    onMount(async () => {
        await fetchTest();
    });

    async function fetchTest() {
        try {
            const res = await fetch(`${API_URL}/api/tests/${testId}`);
            if (res.ok) {
                test = await res.json();
                startTime = Date.now();
            }
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }

    function selectAnswer(questionId, answer) {
        if (showResults) return;
        userAnswers[questionId] = answer;
    }

    function finishTest() {
        showResults = true;
        endTime = Date.now();
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    let score = $derived(
        test?.questions.reduce((acc, q) => {
            return acc + (userAnswers[q.id] === q.correct_answer ? 1 : 0);
        }, 0) || 0,
    );

    let progress = $derived(
        test
            ? (Object.keys(userAnswers).length / test.questions.length) * 100
            : 0,
    );

    function formatTime(ms) {
        const seconds = Math.floor(ms / 1000);
        const minutes = Math.floor(seconds / 60);
        return `${minutes}m ${seconds % 60}s`;
    }

    let isSpeaking = $state(false);
    let currentAudio = null;

    function speak(text) {
        if (!text) return;

        // Stop any current speaking
        if (currentAudio) {
            currentAudio.pause();
            currentAudio = null;
        }

        isSpeaking = true;
        const url = `${API_URL}/api/chat/tts?text=${encodeURIComponent(text)}`;
        const audio = new Audio(url);
        currentAudio = audio;

        audio.play().catch((e) => {
            console.error("Audio playback failed:", e);
            isSpeaking = false;
        });

        audio.onended = () => {
            isSpeaking = false;
        };
    }
</script>

<div class="min-h-screen bg-fd-background flex flex-col">
    <!-- Header / Progress Bar -->
    <header
        class="sticky top-0 z-[100] glass border-b border-fd-border py-4 px-6"
    >
        <div
            class="max-w-[1400px] mx-auto flex items-center justify-between gap-8"
        >
            <div class="flex items-center gap-4">
                <a
                    href="/tests"
                    class="w-10 h-10 rounded-xl bg-fd-secondary border border-fd-border flex items-center justify-center text-fd-muted hover:text-fd-primary transition-all"
                    aria-label="Back to tests"
                >
                    <i class="bx bx-left-arrow-alt text-2xl"></i>
                </a>
                <div class="hidden sm:block">
                    <h2>
                        {test?.title || "Đang tải dữ liệu..."}
                    </h2>
                    <span
                        class="text-[9px] font-bold text-fd-muted uppercase tracking-widest"
                        >Bài kiểm tra {test?.category}</span
                    >
                </div>
            </div>

            <div class="flex-1 max-w-2xl hidden md:block">
                <div
                    class="flex justify-between text-[10px] font-black uppercase tracking-widest text-fd-muted mb-2"
                >
                    <span>Tiến độ Làm bài</span>
                    <span>{Math.round(progress)}%</span>
                </div>
                <div
                    class="h-1.5 w-full bg-fd-secondary rounded-full overflow-hidden"
                >
                    <div
                        class="h-full bg-fd-primary transition-all duration-500 shadow-[0_0_10px_var(--primary-glow)]"
                        style="width: {progress}%"
                    ></div>
                </div>
            </div>

            <div class="flex items-center gap-4">
                {#if !showResults}
                    <button
                        onclick={finishTest}
                        class="fd-btn-primary !py-2 !px-6 !text-[11px] !rounded-xl !font-black !uppercase !tracking-widest shadow-lg shadow-fd-primary/20"
                    >
                        Nộp bài sớm
                    </button>
                {:else}
                    <div class="text-right">
                        <span
                            class="block text-[10px] font-black text-fd-muted uppercase tracking-widest"
                            >Trạng thái</span
                        >
                        <span class="text-fd-primary font-black text-lg"
                            >ĐÃ HOÀN THÀNH</span
                        >
                    </div>
                {/if}
            </div>
        </div>
    </header>

    <main
        class="flex-1 flex flex-col md:flex-row max-w-[1400px] mx-auto w-full p-4 md:p-8 gap-8"
    >
        {#if loading}
            <div class="flex-1 flex flex-col items-center justify-center py-40">
                <div
                    class="w-16 h-16 border-4 border-fd-primary/10 border-t-fd-primary rounded-full animate-spin"
                ></div>
            </div>
        {:else if showResults}
            <!-- Results Pane -->
            <div class="flex-1 space-y-8" in:fade>
                <div
                    class="fd-card !p-12 !rounded-[3rem] text-center bg-fd-primary/5 border-fd-primary/20 relative overflow-hidden"
                >
                    <div class="relative z-10">
                        <div
                            class="w-24 h-24 bg-fd-primary rounded-[2rem] flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-fd-primary/30"
                        >
                            <i class="bx bxs-award text-5xl text-white"></i>
                        </div>
                        <h1
                            class="text-5xl font-[1000] text-fd-foreground tracking-tighter mb-4"
                        >
                            Báo cáo Kết quả
                        </h1>
                        <p
                            class="text-fd-muted font-bold uppercase tracking-[0.2em] text-xs mb-8"
                        >
                            Thống kê Hiệu suất
                        </p>

                        <div
                            class="grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-2xl mx-auto"
                        >
                            <div
                                class="p-6 bg-fd-card rounded-3xl border border-fd-border"
                            >
                                <span
                                    class="block text-[10px] font-black text-fd-muted uppercase tracking-widest mb-2"
                                    >Độ chính xác</span
                                >
                                <span
                                    class="text-4xl font-[1000] text-fd-primary"
                                    >{Math.round(
                                        (score / test.questions.length) * 100,
                                    )}%</span
                                >
                            </div>
                            <div
                                class="p-6 bg-fd-card rounded-3xl border border-fd-border"
                            >
                                <span
                                    class="block text-[10px] font-black text-fd-muted uppercase tracking-widest mb-2"
                                    >Điểm số</span
                                >
                                <span
                                    class="text-4xl font-[1000] text-fd-foreground"
                                    >{score}/{test.questions.length}</span
                                >
                            </div>
                            <div
                                class="p-6 bg-fd-card rounded-3xl border border-fd-border"
                            >
                                <span
                                    class="block text-[10px] font-black text-fd-muted uppercase tracking-widest mb-2"
                                    >Thời gian</span
                                >
                                <span
                                    class="text-2xl font-[1000] text-fd-foreground"
                                    >{formatTime(endTime - startTime)}</span
                                >
                            </div>
                        </div>

                        <button
                            onclick={() => window.location.reload()}
                            class="mt-12 fd-btn-primary !px-12 !py-4 !rounded-2xl !font-black !uppercase !tracking-widest"
                        >
                            Làm lại Bài thi
                        </button>
                    </div>
                    <!-- Bio Background Decor -->
                    <i
                        class="bx bx-dna absolute -right-20 -bottom-20 text-[20rem] text-fd-primary opacity-[0.03] rotate-12"
                    ></i>
                </div>

                <!-- detailed corrections -->
                <div class="space-y-6">
                    <h2
                        class="text-2xl font-black text-fd-foreground tracking-tight ml-4"
                    >
                        Chi tiết Đánh giá
                    </h2>
                    {#each test.questions as q, i}
                        <div
                            class="fd-card !p-8 !rounded-[2.5rem] border {userAnswers[
                                q.id
                            ] === q.correct_answer
                                ? 'border-emerald-500/20 bg-emerald-500/[0.02]'
                                : 'border-red-500/20 bg-red-500/[0.02]'} transition-all"
                        >
                            <div class="flex gap-6">
                                <div
                                    class="w-10 h-10 rounded-xl {userAnswers[
                                        q.id
                                    ] === q.correct_answer
                                        ? 'bg-emerald-500'
                                        : 'bg-red-500'} text-white flex items-center justify-center font-black shrink-0 shadow-lg"
                                >
                                    {i + 1}
                                </div>
                                <div class="flex-1 space-y-4">
                                    <p
                                        class="text-[17px] font-bold text-fd-foreground leading-relaxed"
                                    >
                                        {q.text}
                                    </p>
                                    <div
                                        class="grid grid-cols-1 sm:grid-cols-2 gap-4"
                                    >
                                        <div
                                            class="p-4 rounded-xl bg-fd-background border border-fd-border"
                                        >
                                            <span
                                                class="block text-[9px] font-black text-fd-muted uppercase tracking-widest mb-1"
                                                >Bạn chọn</span
                                            >
                                            <span
                                                class="font-black {userAnswers[
                                                    q.id
                                                ] === q.correct_answer
                                                    ? 'text-emerald-500'
                                                    : 'text-red-500'}"
                                                >{userAnswers[q.id] ||
                                                    "KHÔNG CHỌN"}</span
                                            >
                                        </div>
                                        <div
                                            class="p-4 rounded-xl bg-fd-background border border-fd-border"
                                        >
                                            <span
                                                class="block text-[9px] font-black text-fd-muted uppercase tracking-widest mb-1"
                                                >Đáp án đúng</span
                                            >
                                            <span
                                                class="font-black text-fd-primary"
                                                >{q.correct_answer}</span
                                            >
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        {:else}
            <!-- Test Taking Layout -->
            <div class="flex-1 flex flex-col gap-8">
                <!-- Question Card -->
                {#each [test.questions[currentQuestionIdx]] as q (q.id)}
                    <div
                        class="flex-1 flex flex-col"
                        in:fly={{ y: 20, duration: 400 }}
                    >
                        <div
                            class="fd-card !p-8 md:!p-12 !rounded-[3rem] flex-1 flex flex-col shadow-2xl shadow-fd-primary/5 border-fd-border/50"
                        >
                            <div class="flex items-center gap-4 mb-10">
                                <div
                                    class="px-4 py-1.5 rounded-full bg-fd-primary/10 text-fd-primary text-[10px] font-black uppercase tracking-widest"
                                >
                                    Câu hỏi {currentQuestionIdx + 1} / {test
                                        .questions.length}
                                </div>
                                <div class="h-px flex-1 bg-fd-border/30"></div>
                            </div>

                            <div
                                class="grid grid-cols-1 lg:grid-cols-12 gap-12"
                            >
                                <!-- Textual Inquiry -->
                                <div class="lg:col-span-7 space-y-8">
                                    <div class="flex items-start gap-4">
                                        <h1
                                            class="text-3xl font-black text-fd-foreground leading-tight tracking-tight flex-1"
                                        >
                                            {q.text}
                                        </h1>
                                        <button
                                            onclick={() => speak(q.text)}
                                            class="mt-1 w-10 h-10 rounded-full bg-fd-primary/10 text-fd-primary flex items-center justify-center hover:bg-fd-primary hover:text-white transition-all shrink-0"
                                            title="Nghe câu hỏi"
                                        >
                                            <i class="bx bx-volume-full text-xl"
                                            ></i>
                                        </button>
                                    </div>

                                    <div class="space-y-4">
                                        {#each q.options as opt}
                                            <div
                                                role="button"
                                                tabindex="0"
                                                onclick={() =>
                                                    selectAnswer(q.id, opt)}
                                                onkeydown={(e) =>
                                                    e.key === "Enter" &&
                                                    selectAnswer(q.id, opt)}
                                                class="w-full group relative flex items-center gap-6 p-6 rounded-[2rem] border-2 text-left transition-all duration-300 cursor-pointer
                                                {userAnswers[q.id] === opt
                                                    ? 'bg-fd-primary text-white border-fd-primary shadow-xl shadow-fd-primary/20 scale-[1.02]'
                                                    : 'bg-fd-secondary/30 border-transparent hover:border-fd-primary/30 hover:bg-fd-primary/5'}"
                                            >
                                                <div
                                                    class="w-10 h-10 rounded-xl flex items-center justify-center font-black transition-all
                                                    {userAnswers[q.id] === opt
                                                        ? 'bg-white text-fd-primary'
                                                        : 'bg-fd-card text-fd-muted group-hover:bg-fd-primary group-hover:text-white'}"
                                                >
                                                    {String.fromCharCode(
                                                        65 +
                                                            q.options.indexOf(
                                                                opt,
                                                            ),
                                                    )}
                                                </div>
                                                <span
                                                    class="text-[17px] font-black tracking-tight flex-1"
                                                    >{opt}</span
                                                >
                                                <button
                                                    onclick={(e) => {
                                                        e.stopPropagation();
                                                        speak(opt);
                                                    }}
                                                    class="w-8 h-8 rounded-lg bg-fd-card/50 text-fd-muted flex items-center justify-center hover:text-fd-primary transition-colors relative z-10"
                                                    title="Nghe đáp án"
                                                >
                                                    <i
                                                        class="bx bx-volume-low text-lg"
                                                    ></i>
                                                </button>
                                                {#if userAnswers[q.id] === opt}
                                                    <div
                                                        class="ml-4 w-6 h-6 rounded-full bg-white flex items-center justify-center shrink-0"
                                                        in:scale
                                                    >
                                                        <i
                                                            class="bx bx-check text-fd-primary text-lg"
                                                        ></i>
                                                    </div>
                                                {/if}
                                            </div>
                                        {/each}
                                    </div>
                                </div>

                                <!-- Visual Aid -->
                                <div class="lg:col-span-5">
                                    {#if q.image_data || q.image_url}
                                        <div
                                            class="rounded-[2.5rem] overflow-hidden border border-fd-border shadow-2xl aspect-square relative bg-fd-accent/30 p-2"
                                        >
                                            <img
                                                src={q.image_data ||
                                                    q.image_url}
                                                alt="Medical illustration"
                                                class="w-full h-full object-contain rounded-[2rem]"
                                            />
                                        </div>
                                    {:else}
                                        <div
                                            class="rounded-[2.5rem] border-2 border-dashed border-fd-border/50 h-full min-h-[300px] flex flex-col items-center justify-center p-12 text-center opacity-30 select-none"
                                        >
                                            <i
                                                class="bx bx-atom text-7xl mb-6 animate-spin-slow"
                                            ></i>
                                            <p
                                                class="text-xs font-black uppercase tracking-[0.3em]"
                                            >
                                                Đang xử lý dữ liệu...
                                            </p>
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        </div>
                    </div>
                {/each}

                <!-- Navigation -->
                <div class="flex items-center justify-between gap-6 px-4 pb-8">
                    <button
                        onclick={() =>
                            (currentQuestionIdx = Math.max(
                                0,
                                currentQuestionIdx - 1,
                            ))}
                        disabled={currentQuestionIdx === 0}
                        class="p-5 rounded-2xl bg-fd-card border border-fd-border text-fd-muted hover:text-fd-primary disabled:opacity-30 transition-all shadow-md group"
                        aria-label="Previous question"
                    >
                        <i
                            class="bx bx-left-arrow-alt text-3x group-hover:-translate-x-1 transition-transform"
                        ></i>
                    </button>

                    <div class="hidden sm:flex flex-1 justify-center gap-3">
                        {#each test.questions as _, i}
                            <button
                                onclick={() => (currentQuestionIdx = i)}
                                class="w-10 h-2 rounded-full transition-all duration-300 {i ===
                                currentQuestionIdx
                                    ? 'w-16 bg-fd-primary shadow-[0_0_10px_var(--primary-glow)]'
                                    : userAnswers[test.questions[i].id]
                                      ? 'bg-fd-muted opacity-60'
                                      : 'bg-fd-border'}"
                                aria-label="Go to question {i + 1}"
                            ></button>
                        {/each}
                    </div>

                    {#if currentQuestionIdx < test.questions.length - 1}
                        <button
                            onclick={() => currentQuestionIdx++}
                            class="fd-btn-primary !px-12 !py-5 !rounded-2xl !font-black !uppercase !tracking-widest flex items-center gap-2 group shadow-xl shadow-fd-primary/20"
                        >
                            Câu tiếp theo <i
                                class="bx bx-right-arrow-alt text-xl group-hover:translate-x-1 transition-transform"
                            ></i>
                        </button>
                    {:else}
                        <button
                            onclick={finishTest}
                            class="fd-btn-primary !bg-emerald-500 !px-12 !py-5 !rounded-2xl !font-black !uppercase !tracking-widest flex items-center gap-2 shadow-xl shadow-emerald-500/20"
                        >
                            Nộp Kết quả <i class="bx bx-check-double text-xl"
                            ></i>
                        </button>
                    {/if}
                </div>
            </div>
        {/if}
    </main>
</div>

<style>
    .glass {
        background-color: rgba(var(--background), 0.8);
        backdrop-filter: blur(12px);
    }
    :global(.animate-spin-slow) {
        animation: spin 8s linear infinite;
    }
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
</style>
