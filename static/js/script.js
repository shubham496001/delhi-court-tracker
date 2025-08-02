// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    initializeApplication();
});
// Pseudocode for frontend update
function updateDisplay() {
  document.getElementById('case-type').innerText = document.getElementById('input-case-type').value;
  document.getElementById('case-number').innerText = document.getElementById('input-case-number').value;
  document.getElementById('case-year').innerText = document.getElementById('input-year').value;
}

function initializeApplication() {
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', handleFormSubmit);
    }
    
    // Clear form on page load
    clearSearchResults();
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const { loadingElement, errorElement, resultsElement } = getUIElements();
    
    showLoadingState(loadingElement, errorElement, resultsElement);
    
    try {
        const formData = getFormData(form);
        const response = await fetchCaseDetails(formData);
        
        if (response.status === 'success') {
            displayCaseDetails(response.data);
        } else {
            showErrorMessage(errorElement, response.message || 'Case not found');
        }
    } catch (error) {
        console.error('Search error:', error);
        showErrorMessage(errorElement, 'Failed to fetch case details. Please try again.');
    } finally {
        hideLoadingState(loadingElement);
    }
}

function getUIElements() {
    return {
        loadingElement: document.getElementById('loading'),
        errorElement: document.getElementById('errorMessage'),
        resultsElement: document.getElementById('resultsSection')
    };
}

function showLoadingState(loader, error, results) {
    if (loader) loader.style.display = 'block';
    if (error) error.style.display = 'none';
    if (results) results.style.display = 'none';
}

function hideLoadingState(loader) {
    if (loader) loader.style.display = 'none';
}

function showErrorMessage(element, message) {
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    } else {
        alert(message); // Fallback
    }
}

function getFormData(form) {
    return {
        case_type: form.elements['caseType'].value,
        case_number: form.elements['caseNumber'].value,
        filing_year: form.elements['filingYear'].value
    };
}

async function fetchCaseDetails(formData) {
    const params = new URLSearchParams();
    params.append('case_type', formData.case_type);
    params.append('case_number', formData.case_number);
    params.append('filing_year', formData.filing_year);

    const response = await fetch('/search_case', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
}

function displayCaseDetails(caseData) {
    // Update basic case info
    updateElementText('caseTitle', formatCaseTitle(caseData));
    updateElementText('caseNumberDisplay', formatCaseNumber(caseData));
    updateElementText('petitionerName', caseData.petitioner);
    updateElementText('respondentName', caseData.respondent);
    updateElementText('filingDate', formatDate(caseData.filing_date));
    updateElementText('nextHearingDate', formatDate(caseData.next_hearing) || 'Not scheduled');
    updateElementText('caseStatus', caseData.status || 'Pending');
    updateElementText('presidingJudge', caseData.judge || 'Not assigned');
    
    // Update orders section
    renderCaseOrders(caseData.orders || []);
    
    // Show results
    const resultsElement = document.getElementById('resultsSection');
    if (resultsElement) {
        resultsElement.style.display = 'block';
    }
}

function formatCaseTitle(caseData) {
    if (caseData.case_title) return caseData.case_title;
    const fullType = getCaseTypeFullName(caseData.case_type);
    return `${fullType} No. ${caseData.case_number} of ${caseData.filing_year}`;
}

function formatCaseNumber(caseData) {
    return `${caseData.case_type} ${caseData.case_number}/${caseData.filing_year}`;
}

function formatDate(dateString) {
    if (!dateString) return null;
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-IN', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    } catch {
        return dateString; // Return as-is if not a valid date
    }
}

function updateElementText(id, text) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = text || 'N/A';
    }
}

function renderCaseOrders(orders) {
    const ordersSection = document.querySelector('.orders-section');
    if (!ordersSection) return;
    
    // Clear existing orders (keep the title)
    while (ordersSection.children.length > 1) {
        ordersSection.removeChild(ordersSection.lastChild);
    }
    
    if (orders.length === 0) {
        const noOrders = document.createElement('p');
        noOrders.textContent = 'No orders/judgments found for this case.';
        ordersSection.appendChild(noOrders);
        return;
    }
    
    orders.forEach(order => {
        const orderCard = document.createElement('div');
        orderCard.className = 'order-card';
        orderCard.innerHTML = `
            <div class="order-date">Order Date: ${formatDate(order.date) || 'N/A'}</div>
            <div class="order-description">${order.description || 'No description available'}</div>
            ${order.pdf_link ? 
                `<a href="/download_pdf?url=${encodeURIComponent(order.pdf_link)}" 
                   class="download-btn" 
                   target="_blank">
                    Download Order PDF
                </a>` : 
                '<em>PDF not available</em>'}
        `;
        ordersSection.appendChild(orderCard);
    });
}

function clearSearchResults() {
    const { errorElement, resultsElement } = getUIElements();
    if (errorElement) errorElement.style.display = 'none';
    if (resultsElement) resultsElement.style.display = 'none';
}

function getCaseTypeFullName(abbreviation) {
    const caseTypes = {
        'WP(C)': 'Writ Petition (Civil)',
        'CRL.A': 'Criminal Appeal',
        'FAO': 'First Appeal Order',
        'CS(OS)': 'Civil Suit (Original Side)',
        'ARB.P.': 'Arbitration Petition',
        'TEST.CAS.': 'Testamentary Case',
        'ITA': 'Income Tax Appeal',
        'CO.PET.': 'Company Petition',
        'W.P.(C)': 'Writ Petition (Civil)'
    };
    return caseTypes[abbreviation] || abbreviation;
}