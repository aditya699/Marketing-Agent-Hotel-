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
        document.querySelector('#occupancyRate .large-text').textContent = data.occupancy_rate || '--';
        
        const weatherDisplay = document.querySelector('#weather p');
        weatherDisplay.innerHTML = data.weather ? 
            `<i class="fas fa-${getWeatherIcon(data.weather)}"></i> ${data.weather}` : '--';

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
    }

    function updateResults(data) {
        const personalizedMessages = document.querySelector('#personalizedMessages .content');
        personalizedMessages.innerHTML = '';
        if (data.personalized_messages) {
            data.personalized_messages.forEach(msg => {
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

        const socialMediaContent = document.querySelector('#socialMediaContent .content');
        if (data.social_media_content) {
            socialMediaContent.innerHTML = formatSocialMediaContent(data.social_media_content);
        } else {
            socialMediaContent.innerHTML = '<p>No social media content generated</p>';
        }
    }

    function formatSocialMediaContent(content) {
        const lines = content.split('\n');
        let formattedContent = '';
        let currentItem = '';

        lines.forEach(line => {
            if (line.startsWith('##') || line.startsWith('POSTS:')) {
                if (currentItem) {
                    formattedContent += `<div class="social-media-item">${currentItem}</div>`;
                    currentItem = '';
                }
                currentItem += `<h4>${line.replace('##', '').trim()}</h4>`;
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
            stormy: 'bolt'
        };
        return icons[weather.toLowerCase()] || 'question';
    }
});