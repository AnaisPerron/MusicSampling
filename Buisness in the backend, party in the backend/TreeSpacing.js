// Utility functions for calculations
const calculateDistance = (x1, y1, x2, y2) => {
    return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
};

const countDescendants = (node) => {
    if (!node.children || !node.children.length) return 0;
    return node.children.reduce((sum, child) =>
        sum + 1 + countDescendants(child), 0);
};

const getTreeDepth = (node, currentDepth = 0) => {
    if (!node.children || !node.children.length) return currentDepth;
    return Math.max(...node.children.map(child =>
        getTreeDepth(child, currentDepth + 1)));
};

// Main coordinate generation function
function generateNodeCoordinates({
                                     rootNode,
                                     screenWidth,
                                     screenHeight,
                                     nodeSize,
                                     minSpacing,
                                     initialZoom = 1
                                 }) {
    const coordinates = [];
    const centerX = screenWidth / 2;
    const centerY = screenHeight / 2;

    // Configuration for level-based spacing
    const levelConfig = {
        baseRadius: Math.min(screenWidth, screenHeight) / 4,
        radiusIncrement: Math.min(screenWidth, screenHeight) / 6,
        maxChildrenPerLevel: 10
    };

    // Calculate initial parameters
    const totalDepth = getTreeDepth(rootNode);
    const maxRadius = levelConfig.baseRadius +
        (totalDepth * levelConfig.radiusIncrement);

    // Ensure the layout fits within screen bounds
    const scale = Math.min(
        (screenWidth - nodeSize * 2) / (maxRadius * 2),
        (screenHeight - nodeSize * 2) / (maxRadius * 2)
    ) * initialZoom;

    // Process root node
    coordinates.push({
        id: rootNode.id,
        x: centerX,
        y: centerY,
        level: 0,
        parent: null
    });

    // Recursive function to process each level
    function processLevel(node, level, parentCoord, startAngle, endAngle) {
        if (!node.children || level > 3) return; // Max depth of 4 levels (0-3)

        const children = node.children.slice(0, levelConfig.maxChildrenPerLevel);
        const numChildren = children.length;
        if (numChildren === 0) return;

        // Calculate radius for this level
        const radius = (levelConfig.baseRadius +
            (level * levelConfig.radiusIncrement)) * scale;

        // Calculate spacing based on descendants
        children.forEach((child, index) => {
            const descendants = countDescendants(child);
            const totalDescendants = children.reduce((sum, c) =>
                sum + countDescendants(c), 0);

            // Calculate angular position
            const weightedPosition = descendants /
                (totalDescendants || 1);
            const angleRange = endAngle - startAngle;
            const currentAngle = startAngle +
                (angleRange * (index / numChildren));

            // Calculate coordinates
            const x = centerX + radius * Math.cos(currentAngle);
            const y = centerY + radius * Math.sin(currentAngle);

            // Ensure minimum spacing
            const isValidPosition = coordinates.every(coord =>
                calculateDistance(x, y, coord.x, coord.y) >=
                minSpacing + nodeSize);

            if (isValidPosition) {
                coordinates.push({
                    id: child.id,
                    x,
                    y,
                    level,
                    parent: node.id
                });

                // Calculate angles for next level
                const childStartAngle = currentAngle -
                    (Math.PI / (4 * (level + 1)));
                const childEndAngle = currentAngle +
                    (Math.PI / (4 * (level + 1)));

                // Process next level
                processLevel(
                    child,
                    level + 1,
                    { x, y },
                    childStartAngle,
                    childEndAngle
                );
            }
        });
    }

    // Start processing from root
    processLevel(
        rootNode,
        1,
        { x: centerX, y: centerY },
        0,
        2 * Math.PI
    );

    return coordinates;
}

// Example node data structure
const exampleNode = {
    id: 'root',
    children: [
        {
            id: 'A',
            children: [
                { id: 'A1', children: [{ id: 'A1a' }] },
                { id: 'A2', children: [] }
            ]
        },
        {
            id: 'B',
            children: [
                { id: 'B1', children: [] },
                { id: 'B2', children: [] }
            ]
        }
    ]
};

// Example usage
const result = generateNodeCoordinates({
    rootNode: exampleNode,
    screenWidth: 1920,
    screenHeight: 1080,
    nodeSize: 30,
    minSpacing: 50,
    initialZoom: 1
});