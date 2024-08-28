using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class CameraStreamer : MonoBehaviour
{
    [Header("Cameras")]
    [Tooltip("Reference to the player's or entity's camera")]
    public Camera entityCamera;

    [Header("Cameras")]
    [Tooltip("Reference to the camera used to render the frame (should be disabled)")]
    public Camera feedCamera;

    [Header("Settings")]
    [Tooltip("URL of the Python server")]
    public string serverURL = "http://127.0.0.1:8000/upload"; // Update with your server URL

    // Render texture where the camera will render
    private RenderTexture renderTexture;

    // Texture that will be sent to the Python server
    private Texture2D texture2D;

    void Start()
    {
        // Ensure the feed camera is disabled
        if (feedCamera.enabled)
        {
            Debug.LogError("The 'feedCamera' must be disabled.");
        }

        // Create texture with camera dimensions
        renderTexture = new RenderTexture(entityCamera.pixelWidth, entityCamera.pixelHeight, 24);

        // Set the render texture for the feed camera
        feedCamera.targetTexture = renderTexture;

        // Create a texture to store the captured frame
        texture2D = new Texture2D(renderTexture.width, renderTexture.height, TextureFormat.RGB24, false);
    }

    void Update()
    {
        // Copy the player's camera position and rotation to the feed camera
        feedCamera.transform.position = entityCamera.transform.position;
        feedCamera.transform.rotation = entityCamera.transform.rotation;

        // Capture and send frame if necessary
        StartCoroutine(CaptureAndSendFrame());
    }

    IEnumerator CaptureAndSendFrame()
    {
        yield return new WaitForEndOfFrame();

        // Render the camera
        feedCamera.Render();

        // Read pixels from the texture
        texture2D.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
        texture2D.Apply();

        // Convert the texture to bytes
        byte[] bytes = texture2D.EncodeToJPG();

        // Create a multipart form and add the image file
        var form = new WWWForm();
        form.AddBinaryData("file", bytes, "image.jpg", "image/jpeg");

        using (UnityWebRequest www = UnityWebRequest.Post(serverURL, form))
        {
            www.timeout = 60; // Set timeout to 60 seconds (adjust as needed)

            // Send the request
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                Debug.Log("Image successfully sent and processed.");
                // Handle the response from the server if needed
            }
            else
            {
                Debug.LogError("Error: " + www.error);
            }
        }
    }
}
