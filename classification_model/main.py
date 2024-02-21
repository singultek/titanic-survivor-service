from classification_model.model.lr_pipeline import LRPipeline


def main():
    pipeline = LRPipeline()
    print(f"Initialised pipeline: \n {pipeline.pipeline}")


if __name__ == "__main__":
    main()
