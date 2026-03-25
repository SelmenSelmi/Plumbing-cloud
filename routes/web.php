<?php

use App\Http\Controllers\AdminServiceRequestController;
use App\Http\Controllers\ServiceRequestController;
use Illuminate\Support\Facades\Route;
use Laravel\Fortify\Features;

Route::inertia('/', 'Welcome', [
    'canRegister' => Features::enabled(Features::registration()),
])->name('home');

Route::post('/service-requests', [ServiceRequestController::class, 'store'])
    ->name('service-requests.store');

Route::middleware(['auth', 'verified', 'admin'])->group(function () {
    Route::get('dashboard', [AdminServiceRequestController::class, 'index'])->name('dashboard');
});

require __DIR__.'/settings.php';
