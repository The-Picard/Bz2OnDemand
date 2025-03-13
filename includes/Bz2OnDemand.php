<?php

class Bz2OnDemand {
    public static function onEvent( $article ) {
        $title = $article->getTitle()->getFullText();
        $py_return = exec("python3 extensions/Bz2OnDemand/py_scripts/get_article.py '{$title}'");
        
        if ($py_return === "success") {
            $title_str = Title::newFromText($title);
            $requestContext = RequestContext::getMain();
            $out = $requestContext->getOutput();
            $out->redirect($title_str->getFullURL());
            return false;
        }
        return true; // Returning true allows other hooks to process
    }
}
?>

