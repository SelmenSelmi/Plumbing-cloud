<script setup lang="ts">
import { Head, router } from '@inertiajs/vue3';
import { ref } from 'vue';
import { uploadVideo } from '@/services/videoApi';

const fileInput = ref<HTMLInputElement | null>(null);
const selectedFile = ref<File | null>(null);
const uploadProgress = ref(0);
const isUploading = ref(false);
const errorMessage = ref('');

const openFilePicker = () => {
    fileInput.value?.click();
};

const onFileChanged = (file: File | null) => {
    selectedFile.value = file;
    errorMessage.value = '';
    uploadProgress.value = 0;
};

const onNativeFileChanged = (event: Event) => {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0] ?? null;

    onFileChanged(file);
};

const submit = async () => {
    if (!selectedFile.value) {
        errorMessage.value = 'Please choose an MP4 file.';

        return;
    }

    isUploading.value = true;
    errorMessage.value = '';

    try {
        const video = await uploadVideo(selectedFile.value, (progress) => {
            uploadProgress.value = progress;
        });

        router.visit(`/videos/${video.id}/processing`);
    } catch (error: unknown) {
        errorMessage.value = 'Upload failed. Please retry with a valid MP4 file.';
    } finally {
        isUploading.value = false;
    }
};
</script>

<template>
    <Head title="Create Viral Shorts" />

    <main class="video-shell">
        <section class="video-card">
            <div class="eyebrow">Viral Studio</div>
            <h1 class="hero-title">Turn long videos into vertical viral clips</h1>
            <p class="lead">
                Upload your source video and we will auto-caption, detect facecam/gameplay, and render TikTok/Reels format.
            </p>

            <label class="upload-dropzone" for="video-file">
                <div class="dropzone-icon" aria-hidden="true">⬆</div>
                <div class="dropzone-copy">
                    <div class="dropzone-title">Choose your MP4 file</div>
                    <div class="dropzone-text">
                        Click this box to pick a source video from your computer.
                    </div>
                </div>
                <div class="dropzone-action">Browse files</div>
                <input
                    id="video-file"
                    ref="fileInput"
                    type="file"
                    accept="video/mp4"
                    class="hidden-file-input"
                    @change="onNativeFileChanged"
                />
            </label>

            <div class="selection-row">
                <div v-if="selectedFile" class="selected-file">
                    Selected file: <strong>{{ selectedFile.name }}</strong>
                </div>
                <div v-else class="selected-file muted">
                    No file selected yet.
                </div>
            </div>

            <div v-if="isUploading" class="progress-wrap">
                <progress class="progress-bar" :value="uploadProgress" max="100"></progress>
                <div class="progress-text">Uploading: {{ uploadProgress }}%</div>
            </div>

            <div v-if="errorMessage" class="error-banner">
                {{ errorMessage }}
            </div>

            <div class="actions-row">
                <button
                    class="submit-button"
                    type="button"
                    :disabled="isUploading"
                    @click="submit"
                >
                    {{ isUploading ? 'Uploading...' : 'Upload & Start Processing' }}
                </button>
            </div>
        </section>
    </main>
</template>

<style scoped>
.video-shell {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    background:
        radial-gradient(circle at 20% 20%, rgba(20, 184, 166, 0.15), transparent 40%),
        radial-gradient(circle at 80% 0%, rgba(249, 115, 22, 0.2), transparent 38%),
        linear-gradient(140deg, #f8fafc 0%, #e2e8f0 100%);
}

.video-card {
    width: min(760px, 100%);
    padding: 28px;
    border-radius: 24px;
    border: 1px solid rgba(15, 118, 110, 0.12);
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
    background: rgba(255, 255, 255, 0.84);
    backdrop-filter: blur(12px);
}

.eyebrow {
    color: #155e75;
    text-transform: uppercase;
    letter-spacing: 0.28em;
    font-size: 0.78rem;
    font-weight: 700;
}

.lead {
    margin: 0 0 24px;
    font-size: 1.05rem;
    line-height: 1.6;
    color: #475569;
}

.upload-dropzone {
    display: grid;
    gap: 16px;
    border: 2px dashed rgba(15, 118, 110, 0.28);
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.92);
    padding: 22px;
    cursor: pointer;
    transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}

.upload-dropzone:hover {
    transform: translateY(-1px);
    border-color: rgba(15, 118, 110, 0.52);
    box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
}

.dropzone-icon {
    width: 64px;
    height: 64px;
    display: grid;
    place-items: center;
    border-radius: 999px;
    background: #0f766e;
    color: #ffffff;
    font-size: 1.6rem;
    font-weight: 800;
}

.dropzone-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f172a;
}

.dropzone-text {
    color: #475569;
    line-height: 1.55;
}

.dropzone-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    justify-self: start;
    min-height: 44px;
    padding: 0 16px;
    border-radius: 999px;
    background: #0f766e;
    color: #ffffff;
    font-weight: 700;
    box-shadow: 0 8px 18px rgba(15, 118, 110, 0.24);
}

.selection-row {
    margin-top: 18px;
}

.selected-file {
    color: #0f172a;
}

.selected-file.muted {
    color: #64748b;
}

.progress-wrap {
    margin-top: 18px;
}

.progress-bar {
    width: 100%;
    height: 12px;
    accent-color: #f97316;
}

.progress-text {
    margin-top: 6px;
    font-size: 0.875rem;
    color: #475569;
}

.error-banner {
    margin-top: 18px;
    padding: 12px 14px;
    border-radius: 14px;
    background: #fef2f2;
    color: #b91c1c;
    font-weight: 600;
}

.actions-row {
    margin-top: 22px;
}

.submit-button {
    width: 100%;
    min-height: 52px;
    border: 0;
    border-radius: 16px;
    background: linear-gradient(135deg, #0f766e, #155e75);
    color: #ffffff;
    font-size: 1rem;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 14px 28px rgba(15, 118, 110, 0.22);
}

.submit-button:hover:not(:disabled) {
    filter: brightness(1.04);
}

.submit-button:disabled {
    cursor: progress;
    opacity: 0.7;
}

.hidden-file-input {
    display: none;
}

.hero-title {
    margin: 10px 0 12px;
    font-size: clamp(1.7rem, 4vw, 2.6rem);
    line-height: 1.1;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 1px 0 rgba(15, 23, 42, 0.08);
}
</style>
