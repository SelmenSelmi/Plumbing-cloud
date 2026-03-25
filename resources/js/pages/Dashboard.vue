<script setup lang="ts">
import { Head } from '@inertiajs/vue3';
import AppLayout from '@/layouts/AppLayout.vue';
import { dashboard } from '@/routes';
import type { BreadcrumbItem } from '@/types';

type ServiceRequest = {
    id: number;
    name: string;
    phone: string;
    issue: string;
    status: string;
    created_at: string;
};

defineProps<{
    serviceRequests: ServiceRequest[];
}>();

const breadcrumbs: BreadcrumbItem[] = [
    {
        title: 'Dashboard',
        href: dashboard(),
    },
];

const formatDate = (date: string) => {
    return new Intl.DateTimeFormat('en-US', {
        dateStyle: 'medium',
        timeStyle: 'short',
    }).format(new Date(date));
};
</script>

<template>
    <Head title="Admin Dashboard" />

    <AppLayout :breadcrumbs="breadcrumbs">
        <div class="flex h-full flex-1 flex-col gap-6 p-4 md:p-6">
            <section class="rounded-2xl border border-sidebar-border/70 bg-white p-6 shadow-sm dark:border-sidebar-border dark:bg-sidebar">
                <p class="font-heading text-xs uppercase tracking-[0.2em] text-orange-600">Operations</p>
                <h1 class="font-display mt-2 text-3xl text-slate-900 dark:text-white">Incoming Plumbing Requests</h1>
                <p class="font-heading mt-2 text-slate-600 dark:text-slate-300">
                    Review every guest request submitted from the public website.
                </p>
            </section>

            <section v-if="serviceRequests.length === 0" class="rounded-2xl border border-dashed border-sidebar-border/80 bg-white p-10 text-center dark:border-sidebar-border dark:bg-sidebar">
                <h2 class="font-display text-2xl text-slate-900 dark:text-white">No requests yet</h2>
                <p class="font-heading mt-2 text-slate-600 dark:text-slate-300">New requests will appear here as soon as guests submit the form.</p>
            </section>

            <section v-else class="grid gap-4 md:grid-cols-2">
                <article
                    v-for="request in serviceRequests"
                    :key="request.id"
                    class="rounded-2xl border border-sidebar-border/70 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md dark:border-sidebar-border dark:bg-sidebar"
                >
                    <div class="mb-4 flex items-start justify-between gap-3">
                        <div>
                            <p class="font-display text-xl text-slate-900 dark:text-white">{{ request.name }}</p>
                            <p class="font-heading text-sm text-slate-600 dark:text-slate-300">{{ request.phone }}</p>
                        </div>
                        <span class="rounded-full bg-orange-100 px-3 py-1 font-heading text-xs font-semibold uppercase tracking-[0.14em] text-orange-700">
                            {{ request.status }}
                        </span>
                    </div>

                    <p class="font-heading text-sm leading-relaxed text-slate-700 dark:text-slate-200">{{ request.issue }}</p>

                    <p class="font-heading mt-4 text-xs uppercase tracking-[0.14em] text-slate-500 dark:text-slate-400">
                        Received {{ formatDate(request.created_at) }}
                    </p>
                </article>
            </section>
        </div>
    </AppLayout>
</template>
