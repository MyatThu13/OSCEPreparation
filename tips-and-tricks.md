# Tips & Tricks

```text
this._request("get", "/protected/json/verify/" + token + "/" + id, {}, callback, qs);
```

တစ်ချို.သော user parameter တွေကို URL encode မလုပ်ရင် request module မှာ error ရှိနိုင်။

```text
urllib.quote("#?&=/")  

returns 

%23%3F%26%3D/
```

python ရဲ. urllib က forward slash ကို encode မလုပ်။



