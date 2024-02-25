from classification_model.model.lr_pipeline import LRPipeline


def main():
    pipeline = LRPipeline()
    print(f"Initialised pipeline: \n {pipeline.pipeline}")
    pipeline.train(is_saved=True)


    pipeline.predict()


if __name__ == "__main__":
    main()
