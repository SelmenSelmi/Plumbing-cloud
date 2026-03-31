<?php

use App\Http\Controllers\Api\VideoController;
use Illuminate\Support\Facades\Route;

Route::post('/videos', [VideoController::class, 'store'])->name('api.videos.store');
Route::get('/videos/{video}', [VideoController::class, 'show'])->name('api.videos.show');
Route::get('/videos/{video}/result', [VideoController::class, 'result'])->name('api.videos.result');
