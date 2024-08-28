using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class RealTimeImageSender : MonoBehaviour
{
    public Camera gameCamera;
    public int frameSkip = 5; // Send every 5th frame

    private int frameCounter = 0;

    void Update()
    {
        frameCounter++;
        if (frameCounter >= frameSkip)
        {
            StartCoroutine(SendFrameToServer());
            frameCounter = 0;
        }
    }

    IEnumerator SendFrameToServer()
    {
        // Capture the current frame from the camera
        RenderTexture renderTexture = new RenderTexture(Screen.width, Screen.height, 24);
        gameCamera.targetTexture = renderTexture;
        Texture2D screenShot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
        gameCamera.Render();

        RenderTexture.active = renderTexture;
        screenShot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        screenShot.Apply();

        gameCamera.targetTexture = null;
        RenderTexture.active = null; // Clean up

        byte[] imageBytes = screenShot.EncodeToJPG();

        // Create the form and add the image data
        WWWForm form = new WWWForm();
        form.AddBinaryData("file", imageBytes, "frame.jpg", "image/jpeg");

        // Send the request to the FastAPI server
        using (UnityWebRequest www = UnityWebRequest.Post("http://127.0.0.1:8000/upload/", form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + www.error);
            }
            else
            {
                // Handle the response (e.g., update UI with processed image)
                byte[] responseData = www.downloadHandler.data;
                Texture2D responseTexture = new Texture2D(2, 2);
                responseTexture.LoadImage(responseData);

                // Apply the processed image to a material or UI element
            }
        }
    }
}
