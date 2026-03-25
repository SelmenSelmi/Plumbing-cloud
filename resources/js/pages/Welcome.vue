<script setup lang="ts">
import { Head, Link, useForm, usePage } from '@inertiajs/vue3';
import { dashboard, login, register } from '@/routes';

withDefaults(
    defineProps<{
        canRegister: boolean;
    }>(),
    {
        canRegister: true,
    },
);

const page = usePage();

const form = useForm({
    name: '',
    phone: '',
    issue: '',
});

const submitRequest = () => {
    form.post('/service-requests', {
        preserveScroll: true,
        onSuccess: () => form.reset(),
    });
};
</script>

<template>
    <Head title="Elite Plumbing Services">
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
            rel="preconnect"
            href="https://fonts.gstatic.com"
            crossorigin="anonymous"
        />
        <link
            href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;500;700;800&family=Space+Grotesk:wght@400;500;700&display=swap"
            rel="stylesheet"
        />
    </Head>

    <div class="plumbing-bg min-h-screen text-slate-950">
        <div class="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:px-8">
            <header
                class="mb-8 flex flex-col gap-4 rounded-2xl border border-white/60 bg-white/70 p-4 backdrop-blur md:flex-row md:items-center md:justify-between"
            >
                <div>
                    <p
                        class="font-heading text-sm tracking-[0.2em] text-orange-700 uppercase"
                    >
                        Plumbers Pro
                    </p>
                    <p class="font-display text-xl text-slate-900">
                        Fast, clean, guaranteed repair work
                    </p>
                </div>
                <nav class="flex flex-wrap gap-2">
                    <Link
                        v-if="page.props.auth.user"
                        :href="dashboard()"
                        class="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-orange-400 hover:text-orange-700"
                    >
                        Admin Dashboard
                    </Link>
                    <template v-else>
                        <Link
                            :href="login()"
                            class="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-orange-400 hover:text-orange-700"
                        >
                            Log in
                        </Link>
                        <Link
                            v-if="canRegister"
                            :href="register()"
                            class="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-orange-600"
                        >
                            Create account
                        </Link>
                    </template>
                </nav>
            </header>

            <section class="grid items-center gap-8 lg:grid-cols-[1.1fr_0.9fr]">
                <div class="animate-rise space-y-6">
                    <p
                        class="font-heading inline-flex items-center rounded-full border border-orange-300/60 bg-orange-100/60 px-3 py-1 text-xs tracking-[0.22em] text-orange-700 uppercase"
                    >
                        24/7 Emergency Plumbers
                    </p>
                    <h1
                        class="font-display text-4xl leading-tight sm:text-5xl lg:text-6xl"
                    >
                        The bold plumbing team that gets your water flowing
                        again.
                    </h1>
                    <p
                        class="font-heading max-w-xl text-base text-slate-700 sm:text-lg"
                    >
                        Leak detection, water heater replacement, clogged drain
                        rescue, and full bathroom pipe upgrades. We dispatch
                        quickly and leave the place cleaner than we found it.
                    </p>
                    <div class="flex flex-wrap gap-3">
                        <a
                            href="#request"
                            class="font-heading rounded-full bg-orange-600 px-5 py-3 font-bold text-white shadow-lg shadow-orange-500/30 transition hover:-translate-y-0.5 hover:bg-orange-700"
                        >
                            Request a plumber
                        </a>
                        <span
                            class="font-heading rounded-full border border-slate-300 bg-white px-5 py-3 font-semibold text-slate-800"
                        >
                            Typical response: under 25 minutes
                        </span>
                    </div>
                </div>

                <div
                    class="animate-rise-delayed rounded-[2rem] border border-white/70 bg-white/70 p-6 shadow-xl shadow-slate-900/10 backdrop-blur"
                >
                    <div class="grid gap-4 sm:grid-cols-2">
                        <div class="rounded-2xl bg-slate-900 p-4 text-white">
                            <p class="font-heading text-sm text-slate-300">
                                Jobs completed
                            </p>
                            <p class="font-display text-3xl">4,200+</p>
                        </div>
                        <div class="rounded-2xl bg-orange-500 p-4 text-white">
                            <p class="font-heading text-sm text-orange-100">
                                Local rating
                            </p>
                            <p class="font-display text-3xl">4.9/5</p>
                        </div>
                        <div
                            class="rounded-2xl border border-slate-200 bg-white p-4"
                        >
                            <p class="font-heading text-sm text-slate-500">
                                Non-stop support
                            </p>
                            <p class="font-display text-2xl text-slate-900">
                                365 days
                            </p>
                        </div>
                        <div
                            class="rounded-2xl border border-slate-200 bg-white p-4"
                        >
                            <p class="font-heading text-sm text-slate-500">
                                Arrival window
                            </p>
                            <p class="font-display text-2xl text-slate-900">
                                25 mins
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <section class="mt-12 grid items-start gap-6 lg:grid-cols-2">
                <div
                    class="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-900/5 sm:p-8"
                >
                    <h2 class="font-display text-2xl text-slate-900">
                        Our Services
                    </h2>
                    <p class="font-heading mt-3 text-slate-600">
                        From emergency leaks to full repipes, our certified
                        technicians deliver fast, professional service across
                        the city.
                    </p>
                    <ul class="mt-4 space-y-2 text-sm text-slate-700">
                        <li class="flex items-start gap-3">
                            <span
                                class="mt-2 inline-block h-2 w-2 rounded-full bg-orange-600"
                            ></span>
                            Emergency repairs & leak detection
                        </li>
                        <li class="flex items-start gap-3">
                            <span
                                class="mt-2 inline-block h-2 w-2 rounded-full bg-orange-600"
                            ></span>
                            Drain cleaning & CCTV inspections
                        </li>
                        <li class="flex items-start gap-3">
                            <span
                                class="mt-2 inline-block h-2 w-2 rounded-full bg-orange-600"
                            ></span>
                            Water heater repair & replacement
                        </li>
                        <li class="flex items-start gap-3">
                            <span
                                class="mt-2 inline-block h-2 w-2 rounded-full bg-orange-600"
                            ></span>
                            Bathroom and kitchen repiping
                        </li>
                    </ul>
                    <div class="mt-6 flex gap-3">
                        <a
                            href="#request"
                            class="rounded-full bg-orange-600 px-4 py-2 font-semibold text-white"
                            >Request now</a
                        >
                        <a
                            href="#gallery"
                            class="rounded-full border border-slate-200 px-4 py-2"
                            >See our work</a
                        >
                    </div>
                </div>
                <div
                    id="gallery"
                    class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3"
                >
                    <img
                        loading="lazy"
                        alt="Plumber fixing a pipe"
                        src="https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&q=80&w=600"
                        class="h-40 w-full rounded-2xl object-cover shadow-sm"
                    />

                    <img
                        loading="lazy"
                        alt="Close up of plumbing tools"
                        src="https://images.unsplash.com/photo-1542013936693-884638332954?auto=format&fit=crop&q=80&w=600"
                        class="h-40 w-full rounded-2xl object-cover shadow-sm"
                    />

                    <img
                        loading="lazy"
                        alt="Technician inspecting a water heater"
                        src="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&q=80&w=600"
                        class="h-40 w-full rounded-2xl object-cover shadow-sm"
                    />

                    <img
                        loading="lazy"
                        alt="Newly installed bathroom fixtures"
                        src="https://images.unsplash.com/photo-1585338107529-13afc5f02586?auto=format&fit=crop&q=80&w=600"
                        class="hidden h-40 w-full rounded-2xl object-cover shadow-sm sm:block"
                    />

                    <img
                        loading="lazy"
                        alt="Drain cleaning equipment"
                        src="https://images.unsplash.com/photo-1517646287270-a5a9ca602e5c?auto=format&fit=crop&q=80&w=600"
                        class="hidden h-40 w-full rounded-2xl object-cover shadow-sm lg:block"
                    />

                    <img
                        loading="lazy"
                        alt="Professional faucet installation"
                        src="https://images.unsplash.com/photo-1585938389612-a552a28d6914?auto=format&fit=crop&q=80&w=600"
                        class="hidden h-40 w-full rounded-2xl object-cover shadow-sm lg:block"
                    />
                </div>
            </section>
            <section
                id="request"
                class="mt-14 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]"
            >
                <div
                    class="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-900/5 sm:p-8"
                >
                    <h2 class="font-display text-3xl text-slate-900">
                        Tell us your plumbing issue
                    </h2>
                    <p class="font-heading mt-3 text-slate-600">
                        Share your details and an admin will instantly receive
                        your request from the dashboard.
                    </p>
                    <ul
                        class="font-heading mt-6 space-y-3 text-sm text-slate-700"
                    >
                        <li class="rounded-xl bg-slate-50 px-3 py-2">
                            No account needed to request help.
                        </li>
                        <li class="rounded-xl bg-slate-50 px-3 py-2">
                            You can describe leaks, low pressure, heater faults,
                            and blockages.
                        </li>
                        <li class="rounded-xl bg-slate-50 px-3 py-2">
                            Your phone number helps us dispatch the nearest
                            technician fast.
                        </li>
                    </ul>
                </div>

                <form
                    class="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg shadow-slate-900/5 sm:p-8"
                    @submit.prevent="submitRequest"
                >
                    <div class="grid gap-5">
                        <div>
                            <label
                                class="font-heading mb-2 block text-sm font-semibold text-slate-700"
                                for="name"
                                >Full name</label
                            >
                            <input
                                id="name"
                                v-model="form.name"
                                type="text"
                                required
                                class="font-heading w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 transition outline-none focus:border-orange-500 focus:bg-white"
                                placeholder="John Carter"
                            />
                            <p
                                v-if="form.errors.name"
                                class="mt-1 text-sm text-red-600"
                            >
                                {{ form.errors.name }}
                            </p>
                        </div>

                        <div>
                            <label
                                class="font-heading mb-2 block text-sm font-semibold text-slate-700"
                                for="phone"
                                >Phone number</label
                            >
                            <input
                                id="phone"
                                v-model="form.phone"
                                type="tel"
                                required
                                class="font-heading w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 transition outline-none focus:border-orange-500 focus:bg-white"
                                placeholder="+1 555 123 4567"
                            />
                            <p
                                v-if="form.errors.phone"
                                class="mt-1 text-sm text-red-600"
                            >
                                {{ form.errors.phone }}
                            </p>
                        </div>

                        <div>
                            <label
                                class="font-heading mb-2 block text-sm font-semibold text-slate-700"
                                for="issue"
                                >Issue description</label
                            >
                            <textarea
                                id="issue"
                                v-model="form.issue"
                                rows="5"
                                required
                                class="font-heading w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 transition outline-none focus:border-orange-500 focus:bg-white"
                                placeholder="Describe the plumbing issue in detail..."
                            />
                            <p
                                v-if="form.errors.issue"
                                class="mt-1 text-sm text-red-600"
                            >
                                {{ form.errors.issue }}
                            </p>
                        </div>

                        <p
                            v-if="form.recentlySuccessful"
                            class="font-heading rounded-xl border border-emerald-300 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-700"
                        >
                            Request sent successfully. Our admin team has
                            received it.
                        </p>

                        <button
                            type="submit"
                            :disabled="form.processing"
                            class="font-heading rounded-xl bg-slate-900 px-5 py-3 font-bold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                            {{
                                form.processing ? 'Sending...' : 'Send request'
                            }}
                        </button>
                    </div>
                </form>
            </section>
        </div>
    </div>
</template>
