<?php get_header(); ?>
<?php
if (is_singular()):
    while (have_posts()):
        the_post(); ?>
<?php if (
    is_singular(['target_column', 'target_case']) &&
    !str_contains(get_the_content(), '<h1')
): ?>
<section class="page-hero"><div class="container"><nav class="breadcrumb" aria-label="パンくず"><a href="<?php echo esc_url(
    home_url('/'),
); ?>">TOP</a><span>›</span><a href="<?php echo esc_url(
    get_post_type_archive_link(get_post_type()),
); ?>">
<?php echo is_singular('target_case') ? '導入事例' : 'コラム'; ?>
</a></nav><p class="eyebrow">
<?php echo is_singular('target_case') ? 'CASE STUDY' : 'COLUMN'; ?>
</p><h1>
<?php the_title(); ?>
</h1></div></section><section class="section"><div class="container reading"><p class="byline">執筆：<?php the_author(); ?> ／ 更新日：<?php the_modified_date(); ?>
</p>
<?php if (has_post_thumbnail()) {
    $thumbnail_attributes = ['loading' => 'lazy'];
    the_post_thumbnail('large', $thumbnail_attributes);
} ?>
<?php echo target_one_asset_html(apply_filters('the_content', get_the_content())); ?>
</div></section>
<?php else:echo target_one_asset_html(apply_filters('the_content', get_the_content()));endif; ?>
<?php
    endwhile;
elseif (is_404()): ?>
<section class="section"><div class="container reading"><p class="eyebrow">404</p><h1>ページが見つかりません</h1><p>URLをご確認いただくか、トップページからお探しください。</p><a class="button orange" href="<?php echo esc_url(
    home_url('/'),
); ?>">トップページへ</a></div></section>
<?php else:
    $case = is_post_type_archive('target_case') || is_tax('target_case_industry');
    $type = $case ? 'target_case' : 'target_column';
    $tax = $case ? 'target_case_industry' : 'target_column_category';
    ?>
<section class="page-hero"><div class="container"><nav class="breadcrumb"><a href="<?php echo esc_url(
    home_url('/'),
); ?>">TOP</a><span>›</span><span>
<?php echo $case ? '導入事例' : 'コラム'; ?>
</span></nav><p class="eyebrow">
<?php echo $case ? 'CASE STUDY' : 'COLUMN'; ?>
</p><h1>
<?php echo is_tax() ? esc_html(single_term_title('', false)) : ($case ? '導入事例' : 'コラム'); ?>
</h1><p class="lead">
<?php echo $case
    ? 'Target-Oneの導入事例をご紹介します。※初期掲載はすべてサンプルです。'
    : '競合対策やWeb広告運用など、集客に役立つ情報をお届けします。'; ?>
</p></div></section>
<div class="container filters"><a class="filter" href="<?php echo esc_url(
    get_post_type_archive_link($type),
); ?>">すべて</a>
<?php
$terms = get_terms(['taxonomy' => $tax, 'hide_empty' => true]);
if (!is_wp_error($terms)) {
    foreach ($terms as $term) {
        echo '<a class="filter" href="' .
            esc_url(get_term_link($term)) .
            '">' .
            esc_html($term->name) .
            '</a>';
    }
}
?>
</div>
<section class="section"><div class="container"><div class="cards">
<?php while (have_posts()):
    the_post(); ?>
<a class="card" href="<?php the_permalink(); ?>">
<?php if (has_post_thumbnail()) {
    the_post_thumbnail('medium_large', ['loading' => 'lazy']);
} ?>
<span class="card-index">
<?php echo esc_html(get_the_date()); ?>
</span><h2 style="font-size:18px">
<?php the_title(); ?>
</h2><p>
<?php echo esc_html(get_the_excerpt()); ?>
</p><span class="card-arrow">詳しく見る →</span></a>
<?php
endwhile; ?>
</div>
<?php the_posts_pagination(['prev_text' => '前へ', 'next_text' => '次へ']); ?>
</div></section>
<?php endif;
get_footer();
 ?>
