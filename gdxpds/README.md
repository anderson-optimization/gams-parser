

# [GDX Pandas](https://github.com/NREL/gdx-pandas)

Create docker image to use gdx to csv functionality

Example usage

```bash
docker run -w /root -v $(pwd):/root -u $(id -u):$(id -g) andersonopt/gdxpandas gdx_to_csv.py -i output.gdx -o output 
```
 

## References

Great examples of sandboxing functionality in docker

[https://github.com/jessfraz/dockerfiles](https://github.com/jessfraz/dockerfiles)