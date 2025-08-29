from jobspy_service.app.dedupe import dedupe_jobs


def test_semantic_duplicates_merge() -> None:
    jobs = [
        {
            "title": "Python Developer",
            "description": "Build backend APIs",
        },
        {
            "title": "Backend Engineer",
            "description": "Develop APIs using Python",
        },
        {
            "title": "Graphic Designer",
            "description": "Create visual assets",
        },
    ]
    deduped = dedupe_jobs(jobs)
    assert len(deduped) == 2
    titles = {j["title"] for j in deduped}
    assert "Graphic Designer" in titles
    assert ("Python Developer" in titles) ^ ("Backend Engineer" in titles)

