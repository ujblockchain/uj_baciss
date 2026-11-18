/** Limits the API enforces; checking here saves a wasted upload. */
export const MAX_PHOTO_BYTES = 5 * 1024 * 1024;
export const MAX_AUDIO_BYTES = 10 * 1024 * 1024;

export const PHOTO_ACCEPT = "image/jpeg,image/png,image/webp,.jfif";
export const AUDIO_ACCEPT = "audio/*,.mp3,.m4a,.wav,.ogg,.flac,.webm";
