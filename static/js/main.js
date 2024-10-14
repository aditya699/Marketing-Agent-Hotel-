document.addEventListener('DOMContentLoaded', function() {
    const runAnalysisButton = document.getElementById('runAnalysis');
    const resultsSection = document.getElementById('results');
    const analyzeSentimentButton = document.getElementById('analyzeSentiment');
    const sentimentResultsSection = document.getElementById('sentimentResults');
    const loadingOverlay = document.getElementById('loadingOverlay');

    function updateDashboard() {
        fetch('/get_dashboard_data')
            .then(response => response.json())
            .then(data => {
                document.querySelector('#occupancyRate .large-text').textContent = `${(data.occupancy_rate * 100).toFixed(1)}%`;
                document.querySelector('#weather p').textContent = data.weather || '--';
                
                const campaignList = document.querySelector('#topCampaigns ul');
                campaignList.innerHTML = '';
                if (data.top_campaigns && data.top_campaigns.length > 0) {
                    data.top_campaigns.forEach(campaign => {
                        const li = document.createElement('li');
                        li.textContent = `${campaign.name}: ${campaign.likes} likes`;
                        campaignList.appendChild(li);
                    });
                } else {
                    campaignList.innerHTML = '<li>No campaign data available</li>';
                }

                document.querySelector('#roas #prevRoas').textContent = data.prev_roas.toFixed(2);
                document.querySelector('#roas #targetRoas').textContent = data.target_roas.toFixed(2);
            })
            .catch(error => {
                console.error('Error fetching dashboard data:', error);
                showNotification('Failed to load dashboard data. Please try again.', 'error');
            });
    }

    // Call updateDashboard on page load
    updateDashboard();

    function showLoading() {
        loadingOverlay.style.display = 'flex';
        loadingOverlay.style.opacity = '0';
        setTimeout(() => loadingOverlay.style.opacity = '1', 10);
    }

    function hideLoading() {
        loadingOverlay.style.opacity = '0';
        setTimeout(() => loadingOverlay.style.display = 'none', 300);
    }

    runAnalysisButton.addEventListener('click', function() {
        showLoading();
        fetch('/run_analysis')
            .then(response => response.json())
            .then(data => {
                updateResults(data);
                resultsSection.style.display = 'block';
                hideLoading();
                animateResults();
                // Update dashboard after analysis
                updateDashboard();
            })
            .catch(error => {
                console.error('Error:', error);
                hideLoading();
                showNotification('An error occurred while running the analysis. Please try again.', 'error');
            });
    });

    analyzeSentimentButton.addEventListener('click', function() {
        showLoading();
        fetch('/analyze_sentiment')
            .then(response => response.json())
            .then(data => {
                updateSentimentResults(data);
                sentimentResultsSection.style.display = 'block';
                hideLoading();
                animateResults();
            })
            .catch(error => {
                console.error('Error:', error);
                hideLoading();
                showNotification('An error occurred while analyzing sentiment. Please try again.', 'error');
            });
    });

    function updateResults(data) {
        updatePersonalizedMessages(data.personalized_messages);
        updateSocialMediaContent(data.social_media_content);
        updateCampaignRecommendation(data.campaign_recommendation);
        updateCorporateMessage(data.corporate_message);
    }

    function updatePersonalizedMessages(messages) {
        const personalizedMessages = document.querySelector('#personalizedMessages .content');
        personalizedMessages.innerHTML = '';
        if (messages && messages.length > 0) {
            messages.forEach((msg, index) => {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message-item');
                messageDiv.innerHTML = `
                    <h4>${msg.customer_name} (${msg.customer_email})</h4>
                    <p>${msg.message}</p>
                `;
                messageDiv.style.opacity = '0';
                messageDiv.style.transform = 'translateY(20px)';
                personalizedMessages.appendChild(messageDiv);
                setTimeout(() => {
                    messageDiv.style.transition = 'all 0.5s ease';
                    messageDiv.style.opacity = '1';
                    messageDiv.style.transform = 'translateY(0)';
                }, index * 100);
            });
        } else {
            personalizedMessages.innerHTML = '<p>No personalized messages generated</p>';
        }
    }

    function updateSocialMediaContent(content) {
        const socialMediaContent = document.querySelector('#socialMediaContent .content');
        if (content) {
            socialMediaContent.innerHTML = formatSocialMediaContent(content);
        } else {
            socialMediaContent.innerHTML = '<p>No social media content generated</p>';
        }
    }

    function updateCampaignRecommendation(recommendation) {
        const campaignRecommendation = document.querySelector('#campaignRecommendation .content');
        if (recommendation) {
            const lines = recommendation.split('\n');
            let formattedContent = '';
            lines.forEach((line, index) => {
                const [key, value] = line.split(':');
                if (key && value) {
                    formattedContent += `
                        <div class="recommendation-item" style="opacity: 0; transform: translateY(20px);">
                            <h4>${key.trim()}</h4>
                            <p>${value.trim()}</p>
                        </div>
                    `;
                }
            });
            campaignRecommendation.innerHTML = formattedContent;
            
            setTimeout(() => {
                const items = campaignRecommendation.querySelectorAll('.recommendation-item');
                items.forEach((item, index) => {
                    setTimeout(() => {
                        item.style.transition = 'all 0.5s ease';
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                    }, index * 100);
                });
            }, 100);
        } else {
            campaignRecommendation.innerHTML = '<p>No campaign recommendation generated</p>';
        }
    }

    function updateCorporateMessage(message) {
        const corporateMessageContent = document.querySelector('#corporateMessage .content');
        if (message) {
            corporateMessageContent.innerHTML = `<p class="corporate-message">${message}</p>`;
            const messageElement = corporateMessageContent.querySelector('.corporate-message');
            messageElement.style.opacity = '0';
            messageElement.style.transform = 'translateY(20px)';
            setTimeout(() => {
                messageElement.style.transition = 'all 0.5s ease';
                messageElement.style.opacity = '1';
                messageElement.style.transform = 'translateY(0)';
            }, 100);
        } else {
            corporateMessageContent.innerHTML = '<p>No corporate booking message generated</p>';
        }
    }

    function updateSentimentResults(data) {
        const resultsContainer = document.getElementById('sentimentResults');
        resultsContainer.innerHTML = ''; // Clear previous results

        // Display summary
        const summaryDiv = document.createElement('div');
        summaryDiv.innerHTML = `<h3>Sentiment Summary</h3><pre>${data.summary}</pre>`;
        resultsContainer.appendChild(summaryDiv);

        // Display analysis
        const analysisDiv = document.createElement('div');
        analysisDiv.innerHTML = `<h3>Sentiment Analysis</h3>${marked.parse(data.analysis)}`;
        resultsContainer.appendChild(analysisDiv);

        // Display recent reviews
        const recentReviewsDiv = document.createElement('div');
        recentReviewsDiv.innerHTML = '<h3>Recent Reviews</h3>';
        const reviewsList = document.createElement('ul');
        data.recent_reviews.forEach((review, index) => {
            const reviewItem = document.createElement('li');
            reviewItem.innerHTML = `
                <strong>${review.Date}</strong> (${review.Source}) - 
                <span class="sentiment-${review.Sentiment.toLowerCase()}">${review.Sentiment}</span>
                <br>${review.Comment}
            `;
            reviewItem.style.opacity = '0';
            reviewItem.style.transform = 'translateY(20px)';
            reviewsList.appendChild(reviewItem);
            setTimeout(() => {
                reviewItem.style.transition = 'all 0.5s ease';
                reviewItem.style.opacity = '1';
                reviewItem.style.transform = 'translateY(0)';
            }, index * 100);
        });
        recentReviewsDiv.appendChild(reviewsList);
        resultsContainer.appendChild(recentReviewsDiv);
    }

    function formatSocialMediaContent(content) {
        const lines = content.split('\n');
        let formattedContent = '';
        let currentItem = '';

        lines.forEach((line, index) => {
            if (line.startsWith('REELS:') || line.startsWith('POSTS:')) {
                if (currentItem) {
                    formattedContent += `<div class="social-media-item" style="opacity: 0; transform: translateY(20px);">${currentItem}</div>`;
                    currentItem = '';
                }
                currentItem += `<h4>${line.trim()}</h4>`;
            } else if (line.trim() !== '') {
                currentItem += `<p>${line.trim()}</p>`;
            }
        });

        if (currentItem) {
            formattedContent += `<div class="social-media-item" style="opacity: 0; transform: translateY(20px);">${currentItem}</div>`;
        }

        setTimeout(() => {
            const items = document.querySelectorAll('.social-media-item');
            items.forEach((item, index) => {
                setTimeout(() => {
                    item.style.transition = 'all 0.5s ease';
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, index * 100);
            });
        }, 100);

        return formattedContent;
    }

    function animateResults() {
        const cards = document.querySelectorAll('.result-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateY(0)';
        }, 10);
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-20px)';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
});