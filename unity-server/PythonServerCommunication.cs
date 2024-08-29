using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class RealTimeImageSender : MonoBehaviour
{
    public Camera gameCamera;
    public int frameSkip = 10; // Increase the skip to reduce load
    private int frameCounter = 0;

    private RenderTexture renderTexture;
    private Texture2D screenShot;

    [System.Serializable]
    public class Robot { public int[] position; }
    [System.Serializable]
    public class Containes { public int[] position; }
    [System.Serializable]
    public class Box { public int[] position; }
    [System.Serializable]
    public class RobotContainer
    {
        public List<Robot> robots;
        public List<Container> containers;
        public List<Box> boxes;
    }


    void Start()
    {
        // Initialize and reuse the RenderTexture and Texture2D objects
        renderTexture = new RenderTexture(Screen.width, Screen.height, 24);
        screenShot = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
    }

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
        gameCamera.targetTexture = renderTexture;
        gameCamera.Render();

        RenderTexture.active = renderTexture;
        screenShot.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        screenShot.Apply();

        gameCamera.targetTexture = null;
        RenderTexture.active = null; // Clean up

        byte[] imageBytes = screenShot.EncodeToJPG();
         // Capture the current frame from the camera (existing code)...

        // Serialize robots, containers, and boxes into JSON
        RobotContainer robotContainer = new RobotContainer
        {
            robots = new List<Robot>() { /* Initialize with current positions */ },
            containers = new List<Container>() { /* Initialize with current positions */ },
            boxes = new List<Box>() { /* Initialize with current positions */ }
        };
        string jsonData = JsonUtility.ToJson(robotContainer);

        // Create the form and add image data and JSON
        WWWForm form = new WWWForm();
        form.AddBinaryData("file", imageBytes, "frame.jpg", "image/jpeg");
        form.AddField("jsonData", jsonData);

        // Send the request to the FastAPI server
        using (UnityWebRequest www = UnityWebRequest.Post("http://127.0.0.1:8000/upload/", form))
        {
            www.timeout = 60; // Adjust the timeout if needed
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
                // Example: Apply to a RawImage UI element or a MeshRenderer material
            }
        }
    }

    void OnDestroy()
    {
        // Cleanup
        if (renderTexture != null)
        {
            renderTexture.Release();
        }
        if (screenShot != null)
        {
            Destroy(screenShot);
        }
    }
}
