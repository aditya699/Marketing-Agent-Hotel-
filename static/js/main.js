document.addEventListener('DOMContentLoaded', function() {
    const runAnalysisButton = document.getElementById('runAnalysis');
    const resultsSection = document.getElementById('results');

    runAnalysisButton.addEventListener('click', function() {
        this.classList.add('glow-effect');
        this.textContent = 'Analyzing...';
        
        fetch('/run_analysis')
            .then(response => response.json())
            .then(data => {
                updateDashboard(data);
                updateResults(data);
                resultsSection.style.display = 'block';
                this.classList.remove('glow-effect');
                this.innerHTML = '<i class="fas fa-brain"></i> Initiate AI Analysis';
            })
            .catch(error => {
                console.error('Error:', error);
                this.classList.remove('glow-effect');
                this.innerHTML = '<i class="fas fa-brain"></i> Initiate AI Analysis';
                alert('An error occurred while running the analysis. Please try again.');
            });
    });

    function updateDashboard(data) {
        // Update Occupancy Rate
        document.querySelector('#occupancyRate .large-text').textContent = data.occupancy_rate || '--';
        
        // Update Weather
        const weatherDisplay = document.querySelector('#weather p');
        weatherDisplay.innerHTML = data.weather ? 
            `<i class="fas fa-${getWeatherIcon(data.weather)}"></i> ${data.weather}` : '--';

        // Update Top Campaigns
        const campaignList = document.querySelector('#topCampaigns ul');
        campaignList.innerHTML = '';
        if (data.top_campaigns) {
            Object.entries(data.top_campaigns).forEach(([campaign, likes]) => {
                const li = document.createElement('li');
                li.textContent = `${campaign}: ${likes} likes`;
                campaignList.appendChild(li);
            });
        } else {
            campaignList.innerHTML = '<li>No campaign data available</li>';
        }

        // Update ROAS
        document.getElementById('prevRoas').textContent = data.prev_roas ? data.prev_roas.toFixed(2) : '--';
        document.getElementById('targetRoas').textContent = data.target_roas ? data.target_roas.toFixed(2) : '--';
    }

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
            messages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.innerHTML = `
                    <h4>${msg.customer_name} (${msg.customer_email})</h4>
                    <p>${msg.message}</p>
                `;
                personalizedMessages.appendChild(messageDiv);
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
            lines.forEach(line => {
                const [key, value] = line.split(':');
                if (key && value) {
                    formattedContent += `
                        <div class="recommendation-item">
                            <h4>${key.trim()}</h4>
                            <p>${value.trim()}</p>
                        </div>
                    `;
                }
            });
            campaignRecommendation.innerHTML = formattedContent;
        } else {
            campaignRecommendation.innerHTML = '<p>No campaign recommendation generated</p>';
        }
    }

    function updateCorporateMessage(message) {
        const corporateMessageContent = document.querySelector('#corporateMessage .content');
        if (message) {
            corporateMessageContent.innerHTML = `<p>${message}</p>`;
        } else {
            corporateMessageContent.innerHTML = '<p>No corporate booking message generated</p>';
        }
    }

    function formatSocialMediaContent(content) {
        const lines = content.split('\n');
        let formattedContent = '';
        let currentItem = '';

        lines.forEach(line => {
            if (line.startsWith('REELS:') || line.startsWith('POSTS:')) {
                if (currentItem) {
                    formattedContent += `<div class="social-media-item">${currentItem}</div>`;
                    currentItem = '';
                }
                currentItem += `<h4>${line.trim()}</h4>`;
            } else if (line.trim() !== '') {
                currentItem += `<p>${line.trim()}</p>`;
            }
        });

        if (currentItem) {
            formattedContent += `<div class="social-media-item">${currentItem}</div>`;
        }

        return formattedContent;
    }

    function getWeatherIcon(weather) {
        const icons = {
            sunny: 'sun',
            cloudy: 'cloud',
            rainy: 'cloud-rain',
            stormy: 'bolt',
            cool: 'thermometer-quarter',
            mild: 'thermometer-half',
            warm: 'thermometer-three-quarters',
            humid: 'tint',
            dry: 'sun',
            windy: 'wind',
            calm: 'feather'
        };
        return icons[weather.toLowerCase()] || 'question';
    }
});