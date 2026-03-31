<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\Api\StoreVideoRequest;
use App\Http\Resources\VideoResource;
use App\Http\Resources\VideoResultResource;
use App\Jobs\ProcessVideoJob;
use App\Models\Video;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Str;

class VideoController extends Controller
{
    /**
     * Upload and queue a new video for processing.
     */
    public function store(StoreVideoRequest $request): JsonResponse
    {
        $file = $request->file('video');
        $filename = Str::uuid()->toString().'.mp4';
        $originalPath = $file->storeAs('videos/originals', $filename, 'local');

        $video = Video::query()->create([
            'original_path' => $originalPath,
            'status' => Video::STATUS_PENDING,
        ]);

        ProcessVideoJob::dispatch($video->id)->onQueue('video-processing');

        return (new VideoResource($video))
            ->response()
            ->setStatusCode(201);
    }

    /**
     * Get the current processing status for a video.
     */
    public function show(Video $video): JsonResource
    {
        return new VideoResource($video);
    }

    /**
     * Return processed video URL when available.
     */
    public function result(Video $video): JsonResponse|VideoResultResource
    {
        if ($video->status !== Video::STATUS_COMPLETED || ! $video->processed_path) {
            return response()->json([
                'message' => 'Video is not ready yet.',
                'status' => $video->status,
            ], 409);
        }

        return new VideoResultResource($video);
    }
}
