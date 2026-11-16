<?php
if (!defined('ABSPATH')) {
    exit();
}
add_action('after_setup_theme', function () {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', ['search-form', 'gallery', 'caption', 'style', 'script']);
});
function target_one_register_content()
{
    foreach (
        ['target_case' => ['導入事例', 'case'], 'target_column' => ['コラム', 'column']]
        as $type => $args
    ) {
        register_post_type($type, [
            'labels' => [
                'name' => $args[0],
                'singular_name' => $args[0],
                'add_new_item' => $args[0] . 'を追加',
            ],
            'public' => true,
            'has_archive' => $args[1],
            'rewrite' => ['slug' => $args[1], 'with_front' => false],
            'show_in_rest' => true,
            'supports' => [
                'title',
                'editor',
                'excerpt',
                'thumbnail',
                'author',
                'revisions',
                'custom-fields',
            ],
            'menu_icon' => $type === 'target_case' ? 'dashicons-portfolio' : 'dashicons-edit-page',
        ]);
    }
    register_taxonomy('target_column_category', 'target_column', [
        'label' => 'コラムカテゴリ',
        'public' => true,
        'hierarchical' => true,
        'show_in_rest' => true,
        'rewrite' => ['slug' => 'column/category', 'with_front' => false],
    ]);
    register_taxonomy('target_case_industry', 'target_case', [
        'label' => '業種',
        'public' => true,
        'hierarchical' => true,
        'show_in_rest' => true,
        'rewrite' => ['slug' => 'case/industry', 'with_front' => false],
    ]);
    foreach (['page', 'target_case', 'target_column'] as $type) {
        register_post_meta($type, 'target_one_title', [
            'type' => 'string',
            'single' => true,
            'show_in_rest' => true,
            'sanitize_callback' => 'sanitize_text_field',
            'auth_callback' => fn() => current_user_can('edit_posts'),
        ]);
        register_post_meta($type, 'target_one_description', [
            'type' => 'string',
            'single' => true,
            'show_in_rest' => true,
            'sanitize_callback' => 'sanitize_textarea_field',
            'auth_callback' => fn() => current_user_can('edit_posts'),
        ]);
    }
}
add_action('init', 'target_one_register_content');
function target_one_asset_html($html)
{
    return str_replace('/assets/', esc_url(get_template_directory_uri()) . '/assets/', $html);
}
add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style(
        'target-one',
        get_template_directory_uri() . '/assets/css/style.css',
        [],
        '1.0.0',
    );
    wp_enqueue_script(
        'target-one-config',
        get_template_directory_uri() . '/assets/js/config.js',
        [],
        '1.0.0',
        true,
    );
    wp_enqueue_script(
        'target-one',
        get_template_directory_uri() . '/assets/js/main.js',
        ['target-one-config'],
        '1.0.0',
        true,
    );
});
add_filter('pre_get_document_title', function ($title) {
    if (is_singular()) {
        $custom = get_post_meta(get_queried_object_id(), 'target_one_title', true);
        return ($custom ?: get_the_title()) . ' | Target-One';
    }
    return $title;
});
add_action('wp_head', function () {
    $id = get_queried_object_id();
    $desc = is_singular()
        ? get_post_meta($id, 'target_one_description', true)
        : 'Target-Oneのコラム・導入事例をご紹介します。';
    $url = is_singular()
        ? get_permalink($id)
        : home_url(add_query_arg([], $GLOBALS['wp']->request) . '/');
    echo '<meta name="description" content="' .
        esc_attr($desc) .
        '"><meta property="og:title" content="' .
        esc_attr(wp_get_document_title()) .
        '"><meta property="og:description" content="' .
        esc_attr($desc) .
        '"><meta property="og:url" content="' .
        esc_url($url) .
        '"><meta property="og:type" content="' .
        (is_singular('target_column') ? 'article' : 'website') .
        '"><meta property="og:site_name" content="Target-One"><meta name="twitter:card" content="summary_large_image"><meta property="og:image" content="' .
        esc_url(
            has_post_thumbnail($id)
                ? get_the_post_thumbnail_url($id, 'large')
                : get_template_directory_uri() . '/assets/images/ogp.webp',
        ) .
        '">';
    if (!is_singular()) {
        echo '<link rel="canonical" href="' . esc_url($url) . '">';
    }
    $schema = [
        [
            '@context' => 'https://schema.org',
            '@type' => 'Organization',
            'name' => '株式会社AKINAI',
            'url' => home_url('/'),
        ],
        [
            '@context' => 'https://schema.org',
            '@type' => 'BreadcrumbList',
            'itemListElement' => [
                ['@type' => 'ListItem', 'position' => 1, 'name' => 'TOP', 'item' => home_url('/')],
                [
                    '@type' => 'ListItem',
                    'position' => 2,
                    'name' => is_singular() ? get_the_title($id) : wp_get_document_title(),
                    'item' => $url,
                ],
            ],
        ],
    ];
    if (is_singular('target_column')) {
        $schema[] = [
            '@context' => 'https://schema.org',
            '@type' => 'Article',
            'headline' => get_the_title($id),
            'datePublished' => get_the_date(DATE_W3C, $id),
            'dateModified' => get_the_modified_date(DATE_W3C, $id),
            'author' => [
                '@type' => 'Person',
                'name' => get_the_author_meta('display_name', get_post_field('post_author', $id)),
            ],
            'publisher' => ['@type' => 'Organization', 'name' => '株式会社AKINAI'],
            'mainEntityOfPage' => $url,
        ];
    }
    if (is_singular()) {
        $content = get_post_field('post_content', $id);
        $questions = [];
        if (
            preg_match_all(
                '~<details class="faq"><summary><span>Q</span>(.*?)</summary><div><b>A</b><p>(.*?)</p></div></details>~s',
                $content,
                $matches,
                PREG_SET_ORDER,
            )
        ) {
            foreach ($matches as $m) {
                $questions[] = [
                    '@type' => 'Question',
                    'name' => wp_strip_all_tags($m[1]),
                    'acceptedAnswer' => ['@type' => 'Answer', 'text' => wp_strip_all_tags($m[2])],
                ];
            }
        }
        if ($questions) {
            $schema[] = [
                '@context' => 'https://schema.org',
                '@type' => 'FAQPage',
                'mainEntity' => $questions,
            ];
        }
    }
    echo '<script type="application/ld+json">' .
        wp_json_encode($schema, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) .
        '</script>';
});
add_action('add_meta_boxes', function () {
    foreach (['page', 'target_case', 'target_column'] as $type) {
        add_meta_box(
            'target-one-seo',
            '検索・SNS向け設定',
            function ($post) {
                wp_nonce_field('target_one_seo', 'target_one_seo_nonce');
                foreach (
                    [
                        'title' => 'SEOタイトル（空欄時はページタイトル）',
                        'description' => '検索結果の説明文',
                    ]
                    as $key => $label
                ) {
                    echo '<p><label>' .
                        esc_html($label) .
                        '<br><textarea style="width:100%" name="target_one_' .
                        $key .
                        '">' .
                        esc_textarea(get_post_meta($post->ID, 'target_one_' . $key, true)) .
                        '</textarea></label></p>';
                }
            },
            $type,
        );
    }
});
add_action('save_post', function ($id) {
    if (
        !isset($_POST['target_one_seo_nonce']) ||
        !wp_verify_nonce($_POST['target_one_seo_nonce'], 'target_one_seo') ||
        !current_user_can('edit_post', $id) ||
        wp_is_post_revision($id)
    ) {
        return;
    }
    foreach (['title', 'description'] as $key) {
        if (isset($_POST['target_one_' . $key])) {
            update_post_meta(
                $id,
                'target_one_' . $key,
                sanitize_textarea_field(wp_unslash($_POST['target_one_' . $key])),
            );
        }
    }
});
add_action('after_switch_theme', function () {
    // Existing pages are never overwritten. Sample labels from the wireframe are retained.
    target_one_register_content();
    $seeds = json_decode(file_get_contents(get_template_directory() . '/seed.json'), true);
    usort($seeds, fn($a, $b) => substr_count($a['path'], '/') <=> substr_count($b['path'], '/'));
    foreach ($seeds as $seed) {
        $path = trim($seed['path'], '/');
        $slug = $path === '' ? 'home' : basename($path);
        $type = $seed['type'];
        if ($type === 'page' && get_page_by_path($path === '' ? 'home' : $path, OBJECT, 'page')) {
            continue;
        }
        if ($type !== 'page' && get_page_by_path($slug, OBJECT, $type)) {
            continue;
        }
        $parent = 0;
        if ($type === 'page' && str_contains($path, '/')) {
            $parent_path = dirname($path);
            $ancestor = get_page_by_path($parent_path, OBJECT, 'page');
            if (!$ancestor && $parent_path === 'features') {
                $parent = wp_insert_post([
                    'post_type' => 'page',
                    'post_title' => '機能紹介',
                    'post_name' => 'features',
                    'post_status' => 'publish',
                ]);
            } elseif ($ancestor) {
                $parent = $ancestor->ID;
            }
        }
        $id = wp_insert_post(
            [
                'post_type' => $type,
                'post_title' => html_entity_decode($seed['title'], ENT_QUOTES, 'UTF-8'),
                'post_name' => $slug,
                'post_content' => wp_slash($seed['content']),
                'post_excerpt' => html_entity_decode($seed['description'], ENT_QUOTES, 'UTF-8'),
                'post_status' => 'publish',
                'post_parent' => $parent,
            ],
            true,
        );
        if (is_wp_error($id)) {
            continue;
        }
        update_post_meta(
            $id,
            'target_one_description',
            html_entity_decode($seed['description'], ENT_QUOTES, 'UTF-8'),
        );
        if ($path === '') {
            update_option('show_on_front', 'page');
            update_option('page_on_front', $id);
        }
        if ($type === 'target_column') {
            $category = match ($slug) {
                'remarketing' => '競合対策',
                'cpc', 'quality' => 'Web広告運用',
                'dental' => '業種別集客',
                default => '基礎知識',
            };
            wp_set_object_terms($id, $category, 'target_column_category');
        }
        if ($type === 'target_case') {
            $industry = match ($slug) {
                'gym' => 'ジム・フィットネス',
                'salon' => 'エステ・整体',
                'restaurant' => '飲食店',
                'real-estate' => '不動産・住宅',
                'school' => '教育・スクール',
                default => '歯科・クリニック',
            };
            wp_set_object_terms($id, $industry, 'target_case_industry');
        }
    }
    update_option('permalink_structure', '/%postname%/');
    flush_rewrite_rules();
});

add_action('template_redirect', function () {
    if (is_page('features')) {
        wp_safe_redirect(home_url('/service/'), 301);
        exit();
    }
});

add_action('wp_head', function () {
    $code = trim(get_theme_mod('target_one_search_console', ''));
    if ($code) {
        echo '<meta name="google-site-verification" content="' . esc_attr($code) . '">';
    }
});
add_action('customize_register', function ($customizer) {
    $customizer->add_section('target_one_settings', ['title' => 'Target-One設定']);
    $customizer->add_setting('target_one_search_console', [
        'sanitize_callback' => 'sanitize_text_field',
    ]);
    $customizer->add_control('target_one_search_console', [
        'section' => 'target_one_settings',
        'label' => 'Search Console確認コード（contentの値）',
        'type' => 'text',
    ]);
});
