# Minimize Control Panel Component Sizes
$cssPath = "c:\Users\Bhanu\Desktop\QRoute\frontend\src\components\ControlPanel.css"
$content = Get-Content $cssPath -Raw

# Reduce header padding
$content = $content -replace 'padding: var\(--spacing-xl\);', 'padding: var(--spacing-md);'

# Reduce logo size
$content = $content -replace 'font-size: 2\.5rem;(\s+)width: 56px;(\s+)height: 56px;', 'font-size: 1.75rem;$1width: 40px;$2height: 40px;'
$content = $content -replace 'border-radius: 16px;', 'border-radius: 10px;'

# Reduce title size
$content = $content -replace 'font-size: 1\.65rem;', 'font-size: 1.25rem;'
$content = $content -replace 'font-weight: 800;', 'font-weight: 700;'

# Reduce tagline size
$content = $content -replace '(\.app-tagline \{[^}]*font-size: )0\.8rem;', '${1}0.7rem;'
$content = $content -replace '(\.app-tagline \{[^}]*font-weight: )600;', '${1}500;'
$content = $content -replace '(\.app-tagline \{[^}]*margin: )4px', '${1}2px'

# Reduce section padding
$content = $content -replace '(\.search-section \{[^}]*padding: )var\(--spacing-lg\);', '${1}var(--spacing-md);'
$content = $content -replace '(\.config-section-enhanced \{[^}]*padding: )var\(--spacing-lg\);', '${1}var(--spacing-md);'
$content = $content -replace '(\.action-section-enhanced \{[^}]*padding: )var\(--spacing-lg\);', '${1}var(--spacing-md);'
$content = $content -replace '(\.results-section-minimal \{[^}]*padding: )var\(--spacing-lg\);', '${1}var(--spacing-md);'

# Reduce section title sizes
$content = $content -replace '(\.section-title \{[^}]*font-size: )0\.75rem;', '${1}0.7rem;'
$content = $content -replace '(\.section-title \{[^}]*letter-spacing: )0\.08em;', '${1}0.05em;'

# Reduce search input padding
$content = $content -replace 'padding: 10px 32px 10px 12px;', 'padding: 8px 28px 8px 10px;'
$content = $content -replace '(\.search-input \{[^}]*font-size: )0\.875rem;', '${1}0.8rem;'
$content = $content -replace '(\.search-input \{[^}]*border: )1\.5px', '${1}1px'
$content = $content -replace '(\.search-input \{[^}]*border-radius: )10px;', '${1}8px;'

# Reduce vehicle chip sizes
$content = $content -replace '(\.vehicle-chip \{[^}]*padding: )12px;', '${1}8px;'
$content = $content -replace '(\.vehicle-chip \{[^}]*font-size: )1rem;', '${1}0.85rem;'
$content = $content -replace '(\.vehicle-chip \{[^}]*font-weight: )700;', '${1}600;'
$content = $content -replace '(\.vehicle-chip \{[^}]*border: )1\.5px', '${1}1px'
$content = $content -replace '(\.vehicle-chip \{[^}]*border-radius: )10px;', '${1}6px;'
$content = $content -replace '(\.vehicle-grid \{[^}]*gap: )8px;', '${1}6px;'

# Reduce mode option sizes
$content = $content -replace '(\.mode-option \{[^}]*padding: )12px;', '${1}8px 10px;'
$content = $content -replace '(\.mode-option \{[^}]*border: )1\.5px', '${1}1px'
$content = $content -replace '(\.mode-option \{[^}]*border-radius: )10px;', '${1}6px;'
$content = $content -replace '(\.mode-option \{[^}]*gap: )10px;', '${1}8px;'
$content = $content -replace '(\.mode-toggle \{[^}]*gap: )10px;', '${1}6px;'

# Reduce button sizes
$content = $content -replace 'padding: 14px 20px;', 'padding: 10px 16px;'
$content = $content -replace '(\.btn-optimize-enhanced \{[^}]*font-size: )0\.95rem;', '${1}0.85rem;'
$content = $content -replace '(\.btn-optimize-enhanced \{[^}]*border-radius: )12px;', '${1}8px;'
$content = $content -replace '(\.btn-optimize-enhanced \{[^}]*gap: )8px;', '${1}6px;'

$content = $content -replace 'padding: 14px 16px;', 'padding: 10px 12px;'
$content = $content -replace '(\.btn-clear-enhanced \{[^}]*font-size: )0\.875rem;', '${1}0.8rem;'
$content = $content -replace '(\.btn-clear-enhanced \{[^}]*border-radius: )12px;', '${1}8px;'
$content = $content -replace '(\.btn-clear-enhanced \{[^}]*gap: )6px;', '${1}4px;'
$content = $content -replace '(\.btn-clear-enhanced \{[^}]*border: )1\.5px', '${1}1px'

# Reduce action section gap
$content = $content -replace '(\.action-section-enhanced \{[^}]*gap: )10px;', '${1}8px;'

# Reduce config group gap
$content = $content -replace '(\.config-group \{[^}]*gap: )10px;', '${1}6px;'
$content = $content -replace '(\.config-section-enhanced \{[^}]*gap: )var\(--spacing-lg\);', '${1}var(--spacing-md);'

# Reduce section header margins
$content = $content -replace '(\.section-header \{[^}]*margin-bottom: )10px;', '${1}6px;'
$content = $content -replace '(\.section-header \{[^}]*gap: )6px;', '${1}4px;'

# Save the file
Set-Content $cssPath -Value $content

Write-Host "Control panel sizes minimized successfully!"
