<?php

use App\Models\ServiceRequest;
use App\Models\User;

test('guest can submit a plumbing service request', function () {
    $response = $this->post(route('service-requests.store'), [
        'name' => 'John Carter',
        'phone' => '+1 555 100 2000',
        'issue' => 'My kitchen sink is leaking heavily under the cabinet.',
    ]);

    $response->assertRedirect();

    $this->assertDatabaseHas('service_requests', [
        'name' => 'John Carter',
        'phone' => '+1 555 100 2000',
    ]);
});

test('service request fields are validated', function () {
    $response = $this->post(route('service-requests.store'), [
        'name' => '',
        'phone' => '',
        'issue' => 'short',
    ]);

    $response->assertSessionHasErrors(['name', 'phone', 'issue']);
});

test('admin dashboard shows incoming requests', function () {
    $admin = User::factory()->create(['is_admin' => true]);

    ServiceRequest::query()->create([
        'name' => 'Mary Hill',
        'phone' => '+1 555 333 2222',
        'issue' => 'Water heater stopped producing hot water this morning.',
        'status' => 'new',
    ]);

    $response = $this->actingAs($admin)->get(route('dashboard'));

    $response->assertOk();
    $response->assertSee('Mary Hill');
    $response->assertSee('Water heater stopped producing hot water this morning.');
});
