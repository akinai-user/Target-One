<!doctype html><html <?php language_attributes(); ?>><head><meta charset="<?php bloginfo(
    'charset',
); ?>"><meta name="viewport" content="width=device-width,initial-scale=1"><?php wp_head(); ?></head><body <?php body_class(); ?>><?php
wp_body_open();
echo target_one_asset_html(file_get_contents(get_template_directory() . '/partials/header.html'));
?><main id="main">
