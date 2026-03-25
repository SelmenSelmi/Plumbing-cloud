<?php

namespace App\Http\Controllers;

use App\Models\ServiceRequest;
use Inertia\Inertia;
use Inertia\Response;

class AdminServiceRequestController extends Controller
{
    /**
     * Display all incoming plumbing requests for admins.
     */
    public function index(): Response
    {
        return Inertia::render('Dashboard', [
            'serviceRequests' => ServiceRequest::query()
                ->latest()
                ->get(['id', 'name', 'phone', 'issue', 'status', 'created_at']),
        ]);
    }
}
