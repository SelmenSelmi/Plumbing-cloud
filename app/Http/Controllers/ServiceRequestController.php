<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreServiceRequestRequest;
use App\Models\ServiceRequest;
use Illuminate\Http\RedirectResponse;

class ServiceRequestController extends Controller
{
    /**
     * Store a newly created service request from the public website.
     */
    public function store(StoreServiceRequestRequest $request): RedirectResponse
    {
        ServiceRequest::query()->create($request->validated());

        return back()->with('success', 'Your request has been sent. We will contact you shortly.');
    }
}
