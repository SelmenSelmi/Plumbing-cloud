<?php

namespace App\Services;

use App\Models\Video;
use Illuminate\Http\Client\RequestException;
use Illuminate\Support\Facades\Http;

class VideoProcessingService
{
    /**
     * Send a video to the processing microservice and return the processed path.
     */
    public function process(Video $video): string
    {
        $response = Http::timeout((int) config('services.video_processor.timeout', 600))
            ->post(rtrim(config('services.video_processor.base_url'), '/').'/process-video', [
                'video_path' => storage_path('app/private/'.$video->original_path),
            ]);

        if (! $response->successful()) {
            throw new RequestException($response);
        }

        $processedPath = (string) $response->json('processed_path');

        if ($processedPath === '') {
            throw new \RuntimeException('Video processor did not return processed_path.');
        }

        $normalized = str_replace('\\', '/', $processedPath);
        $privateRoot = str_replace('\\', '/', storage_path('app/private/'));

        if (str_starts_with($normalized, $privateRoot)) {
            $normalized = ltrim(substr($normalized, strlen($privateRoot)), '/');
        }

        return $normalized;
    }
}
