import pytest
from fastapi import UploadFile, BackgroundTasks, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import tempfile
import os

# Import your FastAPI app and the function
from your_app import app, extract_audio_from_video

client = TestClient(app)


@pytest.fixture
def mock_video_file():
    return MagicMock(spec=UploadFile)


@pytest.fixture
def mock_background_tasks():
    return MagicMock(spec=BackgroundTasks)


@pytest.fixture
def mock_temp_file():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        yield temp_file
        os.unlink(temp_file.name)


@patch('your_app.VideoFileClip')
@patch('your_app.tempfile.NamedTemporaryFile')
def test_extract_audio_success(mock_named_temp_file, mock_video_file_clip, mock_video_file, mock_background_tasks, mock_temp_file):
    # Setup mocks
    mock_video_file.read.return_value = b"fake video content"
    mock_named_temp_file.return_value.__enter__.return_value = mock_temp_file
    mock_video_clip = MagicMock()
    mock_video_file_clip.return_value = mock_video_clip
    mock_audio = MagicMock()
    mock_video_clip.audio = mock_audio

    # Call the function
    response = extract_audio_from_video(mock_background_tasks, mock_video_file)

    # Assertions
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'audio/mp3'
    assert response.headers['Content-Disposition'] == 'attachment; filename="extracted_audio.mp3"'

    # Verify mocks were called correctly
    mock_video_file.read.assert_called_once()
    mock_video_file_clip.assert_called_once()
    mock_audio.write_audiofile.assert_called_once()
    mock_video_clip.close.assert_called_once()
    assert mock_background_tasks.add_task.call_count == 2


@patch('your_app.VideoFileClip')
@patch('your_app.tempfile.NamedTemporaryFile')
def test_extract_audio_with_options(mock_named_temp_file, mock_video_file_clip, mock_video_file, mock_background_tasks, mock_temp_file):
    # Setup mocks
    mock_video_file.read.return_value = b"fake video content"
    mock_named_temp_file.return_value.__enter__.return_value = mock_temp_file
    mock_video_clip = MagicMock()
    mock_video_file_clip.return_value = mock_video_clip
    mock_audio = MagicMock()
    mock_video_clip.audio = mock_audio

    # Call the function with options
    response = extract_audio_from_video(
        mock_background_tasks, mock_video_file, output_format="wav", start_time=10, duration=30)

    # Assertions
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'audio/wav'
    assert response.headers['Content-Disposition'] == 'attachment; filename="extracted_audio.wav"'

    # Verify mocks were called correctly
    mock_audio.subclip.assert_called_with(10)
    mock_audio.subclip().subclip.assert_called_with(0, 30)


@patch('your_app.VideoFileClip')
@patch('your_app.tempfile.NamedTemporaryFile')
def test_extract_audio_error(mock_named_temp_file, mock_video_file_clip, mock_video_file, mock_background_tasks, mock_temp_file):
    # Setup mocks to raise an exception
    mock_video_file.read.return_value = b"fake video content"
    mock_named_temp_file.return_value.__enter__.return_value = mock_temp_file
    mock_video_file_clip.side_effect = Exception("Video processing error")

    # Call the function and expect an HTTPException
    with pytest.raises(HTTPException) as exc_info:
        extract_audio_from_video(mock_background_tasks, mock_video_file)

    # Assertions
    assert exc_info.value.status_code == 500
    assert str(exc_info.value.detail) == "Video processing error"

    # Verify temp file cleanup was attempted
    os.unlink.assert_called_once()


def test_extract_audio_endpoint():
    # Test the actual endpoint
    with open("test_video.mp4", "rb") as f:
        response = client.post(
            "/extract-audio/",
            files={"video": ("test_video.mp4", f, "video/mp4")},
            data={"output_format": "wav", "start_time": 5, "duration": 10}
        )

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'audio/wav'
    assert response.headers['Content-Disposition'] == 'attachment; filename="extracted_audio.wav"'
