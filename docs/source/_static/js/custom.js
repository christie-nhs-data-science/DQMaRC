// Define the descriptions and corresponding images for each tile
const descriptions = {
    'tile-completeness': {
        text: 'Completeness refers to the presence of the expected data. Missing data can be represented by empty records, unintended values such as "N/A", or be encoded using specific values such as "999 - Unknown". Missing data indicate over-burdened documentation or incomplete processes, e.g. awaiting for test results.',
        img: '../_static/images/error_completeness.png'
    },
    'tile-validity': {
        text: 'The validity dimension measures if data conforms to predefined standards, patterns, or ranges. Coding standards may be defined by industry standards, such as ISO standards or World Health Organisation standards. Invalid data may indicate a lack of standardised data entry and/or processing, which may lead to a high number of unique values, otherwise known as cardinality.',
        img: '../_static/images/error_validity.png'
    },
    'tile-uniqueness': {
        text: 'Uniqueness ensures each data object, record, or entity is unique where duplication is not expected. The presence of duplicate data may indicate data redundancy and therefore negatively affect the ability to join data in a relational database.',
        img: '../_static/images/error_uniqueness.png'
    },
    'tile-timeliness': {
        text: 'Timeliness assesses whether data is captured in an up-to-date manner. Timely data is crucial for real-time decision-making and operational efficiency. Delayed capture of data, which may occur in manual process-heavy environments, can affect the relevance of that data at a particular point in time. Timeliness can be measured as the difference between the timing of an event being recorded and the time of when that data is captured into a system.',
        img: '../_static/images/error_timeliness.png'
    },
    'tile-consistency': {
        text: 'Consistency is a measure of agreement between data objects within or across datasets. Consistent data may appear as conflicting information captured by different source systems. This indicates the presence of inaccurate data without yet knowing which is correct or most truthful. Inconsistent data may indicate redundant processes.',
        img: '../_static/images/error_consistency.png'
    },
    'tile-accuracy': {
        text: 'Accuracy is a measure of how correctly data describes the real-world object or event. This is achieved by comparing source data with an externally validated, quality assured, and manually curated "gold standard", which acts as the known source of truth.',
        img: '../_static/images/error_accuracy.png'
    }
};

// Function to show description and image
function showDescription(tileId) {
    const descriptionArea = document.getElementById('description-area');
    const descriptionText = document.getElementById('description-text');

    // Get the text and image URL for the clicked tile
    const { text, img } = descriptions[tileId];

    // Update the description text
    descriptionText.innerHTML = text;

    // Add the image below the text
    const descriptionImage = document.createElement('img');
    descriptionImage.src = img;
    descriptionImage.alt = text;

    // Clear previous image if any
    if (descriptionText.nextSibling) {
        descriptionText.nextSibling.remove();
    }

    // Append the new image
    descriptionText.insertAdjacentElement('afterend', descriptionImage);
}

// Add event listeners to the tiles
document.querySelectorAll('.tile').forEach(tile => {
    tile.addEventListener('click', () => {
        showDescription(tile.id);
    });
});