<script setup lang="ts">
import { Head, router } from '@inertiajs/vue3';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { getVideoStatus } from '@/services/videoApi';

const props = defineProps<{
    id: string | number;
}>();

const videoId = computed(() => Number(props.id));
const status = ref<'pending' | 'processing' | 'completed' | 'failed'>('pending');
const isLoading = ref(true);
const errorMessage = ref('');

let pollTimer: number | undefined;

const checkStatus = async () => {
    try {
        const response = await getVideoStatus(videoId.value);
        status.value = response.status;
        errorMessage.value = '';

        if (response.status === 'completed') {
            stopPolling();
            router.visit(`/videos/${videoId.value}/result`);
        }

        if (response.status === 'failed') {
            stopPolling();
            errorMessage.value = 'Processing failed. Please upload again.';
        }
    } catch (error: unknown) {
        errorMessage.value = 'Unable to fetch processing status. Retrying...';
    } finally {
        isLoading.value = false;
    }
};

const startPolling = () => {
    checkStatus();
    pollTimer = window.setInterval(checkStatus, 2500);
};

const stopPolling = () => {
    if (pollTimer) {
        window.clearInterval(pollTimer);
    }
};

onMounted(() => {
    startPolling();
});

onUnmounted(() => {
    stopPolling();
});
</script>

<template>
    <Head title="Processing Video" />

    <q-page class="processing-shell flex flex-center q-pa-md">
        <q-card class="processing-card q-pa-xl text-center">
            <div class="text-overline text-secondary">Rendering</div>
            <h1 class="title q-mt-none q-mb-md">Processing your viral short</h1>

            <q-spinner v-if="status !== 'failed'" color="primary" size="72px" thickness="4" />

            <p class="q-mt-md text-body1 text-grey-8">
                Current status: <strong>{{ status }}</strong>
            </p>

            <q-banner v-if="errorMessage" class="q-mt-md bg-red-1 text-red-9" rounded>
                {{ errorMessage }}
            </q-banner>

            <q-skeleton v-if="isLoading" class="q-mt-lg" type="text" />
        </q-card>
    </q-page>
</template>

<style scoped>
.processing-shell {
    min-height: 100vh;
    background:
        radial-gradient(circle at 5% 15%, rgba(14, 165, 233, 0.22), transparent 38%),
        radial-gradient(circle at 85% 80%, rgba(251, 146, 60, 0.2), transparent 42%),
        linear-gradient(145deg, #ecfeff 0%, #f8fafc 60%, #eef2ff 100%);
}

.processing-card {
    width: min(640px, 100%);
    border-radius: 24px;
    border: 1px solid rgba(14, 116, 144, 0.14);
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
}

.title {
    font-size: clamp(1.5rem, 4vw, 2.2rem);
    line-height: 1.15;
    font-weight: 800;
}
</style>
