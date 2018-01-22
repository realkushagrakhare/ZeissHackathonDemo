using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class ImageDisplayer : MonoBehaviour {

    public Image image;
    private string url = "https://imagezeiss.blob.core.windows.net/vrone/yesno.jpg";
    private float time = 0.0f;
    // Use this for initialization

    IEnumerator Start()
    {
        time = 0;
        Texture2D tex;
        tex = new Texture2D(4, 4, TextureFormat.DXT1, false);
        using (WWW www = new WWW(url))
        {
            yield return www;
            www.LoadImageIntoTexture(tex);
            image.sprite = Sprite.Create(www.texture, new Rect(0, 0, www.texture.width, www.texture.height), new Vector2(0, 0));
            //GetComponent<Renderer>().material.mainTexture = tex;
        }
    }

    // Update is called once per frame
    void Update () {
        time += Time.deltaTime;
        Debug.Log(time);
        if (time > 5f) 
        {
            time -= 5f;
            //loadTexture();
            Transform parent = image.transform.parent;
            Image clone = Instantiate(image, parent);
            image.transform.parent = null;
            Destroy(image);
        }
	}

    IEnumerator loadTexture(){
        Texture2D tex;
        tex = new Texture2D(4, 4, TextureFormat.DXT1, false);
        string url2 = "http://static.flickr.com/2139/2187478724_6a311bc76f.jpg";
        Texture2D myTexture = Resources.Load<Texture2D>(url2);
        Sprite sprite = Sprite.Create(myTexture, new Rect(0, 0, myTexture.width, myTexture.height), new Vector2(0.5f, 0.5f));
        image.sprite = sprite;
        using (WWW www = new WWW(url2))
        {
            //Debug.Log(time);
            yield return www;
            www.LoadImageIntoTexture(tex);
            Sprite s = Sprite.Create(www.texture, new Rect(0, 0, www.texture.width, www.texture.height), Vector2.zero, 0);
            // image.sprite = Sprite.Create(www.texture, new Rect(0, 0, www.texture.width, www.texture.height), new Vector2(0, 0));
            image.GetComponent<SpriteRenderer>().sprite = s;
            //GetComponent<Renderer>().material.mainTexture = tex;
        }
    }
}
