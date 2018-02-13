# Run with Docker

save planned elements:
```bash
docker build . -t element-extractor
docker run -e ENVIRONMENT=acceptance -e AVVIR_FLOOR=[your floor id here] -v [path to ifc directory]:/workspace element-extractor --ifc /workspace/[your-ifc.ifc]
```

save scanned elements:
```bash
docker build . -t element-extractor
docker run -e ENVIRONMENT=acceptance -e AVVIR_SCAN_ID=[your scan id here] -v [path to ifc directory]:/workspace element-extractor --ifc /workspace/[your-ifc.ifc] --progress
```


access the container interactively:
```bash
docker build . -t element-extractor
docker run -it --entrypoint bash element-extractor
```