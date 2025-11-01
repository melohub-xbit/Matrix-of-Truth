db.game_pairs.insertMany([
    {
        id: "pair-001",
        items: [
            {
                id: "item-1",
                type: "article",
                title: "Local Weather Service Predicts Mild Summer",
                url: "https://example.com/weather",
                excerpt: "Meteorologists at the National Weather Service predict...",
                is_fake: false,
                explanation: "This article comes from a verified weather service and includes specific, verifiable predictions and expert quotes."
            },
            {
                id: "item-2",
                type: "article",
                title: "Scientists Discover Weather Control Device",
                url: "https://example.biz/weather-control",
                excerpt: "A revolutionary device that can control the weather...",
                is_fake: true,
                explanation: "This article makes extraordinary claims without evidence, uses a suspicious domain (.biz), and has no verifiable sources."
            }
        ]
    }
    // Add more pairs as needed
]);