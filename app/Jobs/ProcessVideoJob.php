<?php

namespace App\Jobs;

use App\Models\Video;
use App\Services\VideoProcessingService;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessVideoJob implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(public int $videoId) {}

    /**
     * Execute the job.
     */
    public function handle(VideoProcessingService $videoProcessingService): void
    {
        $video = Video::query()->find($this->videoId);

        if (! $video) {
            return;
        }

        $video->forceFill([
            'status' => Video::STATUS_PROCESSING,
        ])->save();

        try {
            $processedPath = $videoProcessingService->process($video);

            $video->forceFill([
                'status' => Video::STATUS_COMPLETED,
                'processed_path' => $processedPath,
            ])->save();
        } catch (\Throwable) {
            $video->forceFill([
                'status' => Video::STATUS_FAILED,
            ])->save();
        }
    }
}
