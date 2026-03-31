<script setup lang="ts">
import { Head } from '@inertiajs/vue3';
import { computed, onMounted, ref } from 'vue';
import { getVideoResult } from '@/services/videoApi';

const props = defineProps<{
    id: string | number;
}>();

const videoId = computed(() => Number(props.id));
const processedUrl = ref('');
const isLoading = ref(true);
const errorMessage = ref('');

const loadResult = async () => {
    isLoading.value = true;

    try {
        const response = await getVideoResult(videoId.value);

        if (!response.processed_url) {
            errorMessage.value = 'Processed video URL is missing.';
        } else {
            processedUrl.value = response.processed_url;
            errorMessage.value = '';
        }
    } catch (error: unknown) {
        errorMessage.value = 'Result is not ready. Please return to processing page.';
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    loadResult();
});
</script>

<template>
    <Head title="Video Ready" />

    <q-page class="result-shell q-pa-md">
        <div class="row justify-center">
            <div class="col-12 col-md-10 col-lg-8">
                <q-card class="q-pa-lg result-card">
                    <div class="text-overline text-accent">Done</div>
                    <h1 class="title q-mt-none q-mb-sm">Your vertical video is ready</h1>
                    <p class="q-mt-none q-mb-lg text-grey-8">
                        Review the generated short below and download it to publish on TikTok, Reels, or Shorts.
                    </p>

                    <q-skeleton v-if="isLoading" type="rect" height="520px" />

                    <q-banner v-else-if="errorMessage" class="bg-red-1 text-red-9 q-mb-md" rounded>
                        {{ errorMessage }}
                    </q-banner>

                    <q-video
                        v-else
                        :ratio="9 / 16"
                        :src="processedUrl"
                        class="rounded-borders q-mb-md"
                    />

                    <div class="row q-col-gutter-sm">
                        <div class="col-12 col-sm-6">
                            <q-btn
                                v-if="processedUrl"
                                class="full-width"
                                color="secondary"
                                unelevated
                                icon="download"
                                label="Download Video"
                                type="a"
                                :href="processedUrl"
                                target="_blank"
                            />
                        </div>
                    </div>
                </q-card>
            </div>
        </div>
    </q-page>
</template>

<style scoped>
.result-shell {
    min-height: 100vh;
    background:
        radial-gradient(circle at 0% 0%, rgba(251, 146, 60, 0.2), transparent 35%),
        radial-gradient(circle at 90% 20%, rgba(13, 148, 136, 0.2), transparent 36%),
        linear-gradient(160deg, #fff7ed 0%, #f8fafc 58%, #ecfeff 100%);
}

.result-card {
    border-radius: 24px;
    border: 1px solid rgba(251, 146, 60, 0.2);
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
}

.title {
    font-size: clamp(1.5rem, 4vw, 2.2rem);
    line-height: 1.15;
    font-weight: 800;
}
</style>
