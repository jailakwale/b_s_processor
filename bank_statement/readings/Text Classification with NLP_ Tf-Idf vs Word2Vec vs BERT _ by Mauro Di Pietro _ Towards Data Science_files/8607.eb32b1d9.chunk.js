(self.webpackChunklite=self.webpackChunklite||[]).push([[8607],{43915:(e,t,n)=>{"use strict";n.d(t,{Z:()=>l});var r=n(67294);function o(){return(o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}var i=r.createElement("path",{d:"M19.07 21.12a6.33 6.33 0 0 1-3.53-1.1 7.8 7.8 0 0 1-.7-.52c-.77.21-1.57.32-2.38.32-4.67 0-8.46-3.5-8.46-7.8C4 7.7 7.79 4.2 12.46 4.2c4.66 0 8.46 3.5 8.46 7.8 0 2.06-.85 3.99-2.4 5.45a6.28 6.28 0 0 0 1.14 2.59c.15.21.17.48.06.7a.69.69 0 0 1-.62.38h-.03zm0-1v.5l.03-.5h-.03zm-3.92-1.64l.21.2a6.09 6.09 0 0 0 3.24 1.54 7.14 7.14 0 0 1-.83-1.84 5.15 5.15 0 0 1-.16-.75 2.4 2.4 0 0 1-.02-.29v-.23l.18-.15a6.6 6.6 0 0 0 2.3-4.96c0-3.82-3.4-6.93-7.6-6.93-4.19 0-7.6 3.11-7.6 6.93 0 3.83 3.41 6.94 7.6 6.94.83 0 1.64-.12 2.41-.35l.28-.08z",fillRule:"evenodd"});const l=function(e){return r.createElement("svg",o({width:25,height:25},e),i)}},55459:(e,t,n)=>{"use strict";n.d(t,{Z:()=>l});var r=n(67294);function o(){return(o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}var i=r.createElement("path",{d:"M21.27 20.06a9.04 9.04 0 0 0 2.75-6.68C24.02 8.21 19.67 4 14.1 4S4 8.21 4 13.38c0 5.18 4.53 9.39 10.1 9.39 1 0 2-.14 2.95-.41.28.25.6.49.92.7a7.46 7.46 0 0 0 4.19 1.3c.27 0 .5-.13.6-.35a.63.63 0 0 0-.05-.65 8.08 8.08 0 0 1-1.29-2.58 5.42 5.42 0 0 1-.15-.75zm-3.85 1.32l-.08-.28-.4.12a9.72 9.72 0 0 1-2.84.43c-4.96 0-9-3.71-9-8.27 0-4.55 4.04-8.26 9-8.26 4.95 0 8.77 3.71 8.77 8.27 0 2.25-.75 4.35-2.5 5.92l-.24.21v.32a5.59 5.59 0 0 0 .21 1.29c.19.7.49 1.4.89 2.08a6.43 6.43 0 0 1-2.67-1.06c-.34-.22-.88-.48-1.16-.74z"});const l=function(e){return r.createElement("svg",o({width:29,height:29},e),i)}},14345:(e,t,n)=>{"use strict";n.d(t,{A:()=>$,r:()=>X});var r=n(28655),o=n.n(r),i=n(71439),l=n(67294),a=n(67154),s=n.n(a),c=n(63038),u=n.n(c),d=n(12291),p=n(93653),f=n(35848),v=n(53962),m=n(63564),b=n(71245),h=n(965),E=n(78820),C=n(73232),y=n(76532),P=n(1932),w=n(32262),S=n(57469),g=n(23824),O=n(29169),T=n(92528),I=n(80362),k=n(82318),x=n(77601),R=n(98024),j=n(6688),D=n(14391),V=n(65347),L=n(67297),F=n(93394),_=n(39171),A=n(51064),M=n(55573),U=n(27952);function B(){var e=o()(["\n  fragment TruncatedPostCardEditorWriterButton_post on Post {\n    id\n    collection {\n      id\n      name\n      slug # Needed for rejectPostFromPub (not currently exposed as a reusable fragment)\n    }\n    allowResponses\n    clapCount\n    visibility\n    mediumUrl\n    responseDistribution\n    ...useIsPinnedInContext_post\n    ...CopyFriendLinkMenuItem_post\n    ...ClapMutation_post\n  }\n  ","\n  ","\n  ","\n"]);return B=function(){return e},e}var K=function(e){return{fill:e.baseColor.fill.normal,":hover":{fill:e.baseColor.fill.darker},":focus":{fill:e.baseColor.fill.darker}}},z=function(e){var t=e.post,n=e.publisherContext,r=e.isEditor,o=e.isWriter,i=e.creator,a=(0,j.I)(),c=(0,L.v9)((function(e){return e.config.authDomain})),B=t.id,z=t.collection,N=t.responseDistribution,Q=t.visibility,W=t.mediumUrl,H=t.allowResponses,J=(0,y.H)().value,Z=null==J?void 0:J.id,G=null==i?void 0:i.id,q=(0,P.Tf)(t).viewerEdge,$=z||{id:"",name:""},X=$.id,Y=$.name,ee=(0,A.O)(!1),te=u()(ee,3),ne=te[0],re=te[1],oe=te[2],ie=(0,E.n_)(t,n),le=u()(ie,2),ae=le[0],se=le[1],ce=l.useState(""),ue=u()(ce,2),de=ue[0],pe=ue[1],fe=l.useCallback((function(){oe(),se().then((function(e){var t=e.errors;t&&t.length&&t[0].message?pe(t[0].message):window.location.reload()}))}),[oe,se,pe]),ve=(0,b.yb)(t),me=(0,A.O)(!1),be=u()(me,3),he=be[0],Ee=be[1],Ce=be[2],ye=l.useCallback((function(){ve(z).then((function(){return window.location.reload()}))}),[X,ve]),Pe=(0,p.j)(B),we=u()(Pe,1)[0],Se=(0,A.O)(!1),ge=u()(Se,3),Oe=ge[0],Te=ge[1],Ie=ge[2],ke=l.useCallback((function(){we().then((function(){return window.location.reload()}))}),[we]),xe=N===D.Et.DISTRIBUTED,Re=(0,A.O)(!1),je=u()(Re,3),De=je[0],Ve=je[1],Le=je[2],Fe={buttonStyle:"ERROR",cancelText:"Cancel"},_e="truncatedPostCardEditorWriterMenu",Ae="Delete story".concat(xe?" and response":""),Me=xe?C.Q:"Are you sure you want to delete this story?",Ue="LOCKED"===Q,Be="User"===n&&o||"Collection"===n&&r,Ke=(0,d.I0)(),ze=l.useCallback((function(e){return Ke((0,V.at)(e))}),[Ke]),Ne=(0,L.b$)((function(e){return e.multiVote.clapsPerPost})),Qe=(0,M.l)(Ne,t,q),We=Qe.clapCount,He=Qe.viewerClapCount,Je=(0,h.CP)();return l.createElement(l.Fragment,null,l.createElement(T.Q,s()({},Fe,{isVisible:he,onConfirm:ye,hide:Ce,titleText:"Remove story",confirmText:"Remove",isDestructiveAction:!0}),"Are you sure you want to remove this story from ",Y,"?"),l.createElement(T.Q,s()({},Fe,{isVisible:Oe,onConfirm:ke,hide:Ie,titleText:Ae,confirmText:"Delete",isDestructiveAction:!0}),Me),l.createElement(T.Q,{buttonStyle:"STRONG",cancelText:"Cancel",isVisible:De,onConfirm:function(){var e=(0,U.d0A)(c,B);window.location.replace(e)},hide:Le,titleText:"Edit story and response",confirmText:"Continue",isDestructiveAction:!1},C.t),l.createElement(I.J,{ariaId:_e,hide:oe,isVisible:ne,popoverRenderFn:function(){return l.createElement(w.mX,null,l.createElement(w.Sl,null,xe?l.createElement(k.r,{linkStyle:"SUBTLE",onClick:(0,_.B)(oe,Ve)},"Edit story"):l.createElement(k.r,{linkStyle:"SUBTLE",href:(0,U.d0A)(c,B)},"Edit story")),(r||o&&"User"===n)&&l.createElement(w.Sl,null,l.createElement(k.r,{onClick:fe},ae?"Unpin":"Pin"," story")),l.createElement(w.oK,null),l.createElement(w.Sl,null,l.createElement(k.r,{href:(0,U.KIb)(c,B)},"Story settings")),l.createElement(w.Sl,null,l.createElement(k.r,{href:(0,U.T0G)(c,B)},"Story stats")),Ue&&W&&(null==q?void 0:q.shareKey)&&l.createElement(v.$,{post:t,shareKey:null==q?void 0:q.shareKey}),l.createElement(w.oK,null),Be?l.createElement(m.r,{hidePopover:oe,postId:t.id,allowResponses:H}):null,X&&l.createElement(w.Sl,null,l.createElement(k.r,{onClick:Ee},"Remove story from publication")),o&&l.createElement(w.Sl,null,l.createElement(k.r,{onClick:(0,_.B)(oe,Te)},"Delete story")),r&&!o&&l.createElement(l.Fragment,null,l.createElement(w.oK,null),Z&&We&&He&&He>0?l.createElement(w.Sl,null,l.createElement(k.r,{onClick:function(){return Je(t,(null==J?void 0:J.id)||"",-He,q),ze({postId:t.id,clapCount:We-He,viewerClapCount:0,viewerHasClappedSinceFetch:!0}),void oe()}},"Undo applause for this post")):null,l.createElement(O.z,{targetUserId:G,postId:t.id,hidePopover:oe,viewerId:Z}),l.createElement(f.qT,{hidePopover:oe,creator:i}),l.createElement(S.F,{hidePopover:oe,creator:i,viewer:J}),l.createElement(g.j,{hidePopover:oe,creator:i,viewer:J})))}},l.createElement(k.r,{ariaControls:_e,ariaExpanded:ne?"true":"false",ariaLabel:"More options",onClick:re},l.createElement(F.Z,{className:a(K)}))),l.createElement(x.F,{isVisible:!!de,hide:function(){return pe("")},duration:5e3},l.createElement(R.F,{scale:"M"},de)))},N=(0,i.Ps)(B(),E.xt,v.g,h.JP),Q=n(36511);function W(){var e=o()(["\n  fragment TruncatedPostCardReaderButton_post on Post {\n    id\n    collection {\n      id\n    }\n    creator {\n      id\n    }\n    clapCount\n    ...ClapMutation_post\n  }\n  ","\n"]);return W=function(){return e},e}var H=function(e){return{fill:e.baseColor.fill.normal,":hover":{fill:e.baseColor.fill.darker},":focus":{fill:e.baseColor.fill.darker}}},J=function(e){var t=e.post,n=e.viewer,r=(0,j.I)(),o=t.creator,i=null==o?void 0:o.id,a=(0,A.O)(!1),s=u()(a,3),c=s[0],p=s[1],v=s[2],m="truncatedPostCardReaderMenu",b=(0,Q.r)().viewerId,E=(0,P.Tf)(t).viewerEdge,C=(0,d.I0)(),y=l.useCallback((function(e){return C((0,V.at)(e))}),[C]),T=(0,L.b$)((function(e){return e.multiVote.clapsPerPost})),x=(0,M.l)(T,t,E),R=x.clapCount,D=x.viewerClapCount,_=(0,h.CP)();if(!i)return null;var U=b&&R&&D&&D>0;return l.createElement(I.J,{ariaId:m,hide:v,isVisible:c,popoverRenderFn:function(){return l.createElement(w.mX,null,!!U&&l.createElement(w.Sl,null,l.createElement(k.r,{onClick:function(){return _(t,(null==n?void 0:n.id)||"",-D,E),y({postId:t.id,clapCount:R-D,viewerClapCount:0,viewerHasClappedSinceFetch:!0}),void v()}},"Undo applause for this post")),l.createElement(O.z,{targetUserId:i,postId:t.id,hidePopover:v,viewerId:b}),l.createElement(f.qT,{hidePopover:v,creator:o}),l.createElement(S.F,{hidePopover:v,creator:o,viewer:n}),l.createElement(g.j,{hidePopover:v,creator:o,viewer:n}))}},l.createElement(k.r,{ariaControls:m,ariaExpanded:c?"true":"false",ariaLabel:"More options",onClick:p},l.createElement(F.Z,{className:r(H)})))},Z=(0,i.Ps)(W(),h.JP),G=n(73891);function q(){var e=o()(["\n  fragment TruncatedPostCardOverflowButton_post on Post {\n    creator {\n      id\n    }\n    ...TruncatedPostCardEditorWriterButton_post\n    ...TruncatedPostCardReaderButton_post\n  }\n  ","\n  ","\n"]);return q=function(){return e},e}var $=function(e){var t=e.post,n=e.publisherContext,r=(0,y.H)().value,o=(0,G.gY)(t.collection).viewerEdge,i=!(null==o||!o.isEditor),a=t.creator,s=(null==r?void 0:r.id)===(null==a?void 0:a.id);return r?i||s?l.createElement(z,{post:t,isEditor:i,isWriter:s,publisherContext:n,creator:a}):l.createElement(J,{post:t,viewer:r}):null},X=(0,i.Ps)(q(),N,Z)},40917:(e,t,n)=>{"use strict";n.d(t,{e:()=>p});var r=n(59713),o=n.n(r),i=n(4743),l=n(14391),a=n(43198);function s(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function c(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?s(Object(n),!0).forEach((function(t){o()(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):s(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var u=function(e,t){var n;return t?c(c({},e),{},{markups:[{anchorType:l.yG.LINK,type:l.Jh.A,start:0,end:(null==e||null===(n=e.text)||void 0===n?void 0:n.length)||0,href:t,userId:null,linkMetadata:null}]}):e},d=function(e,t){return t?c(c({},e),{},{href:t}):e},p=function(e,t){var n,r=!(arguments.length>2&&void 0!==arguments[2])||arguments[2],o=null!==(n=(0,i.LI)(e).titleIndex)&&void 0!==n?n:(0,a.s)(e,a.j);return e.map((function(e,n){return r&&e.type===l.NJ.IMG?d(e,t):n===o?u(e,t):e}))}},30570:(e,t,n)=>{"use strict";n.d(t,{sK:()=>v,L0:()=>m,q9:()=>b});var r=n(28655),o=n.n(r),i=n(63038),l=n.n(i),a=n(71439),s=n(67294),c=n(73788),u=n(53976),d=n(12388);function p(){var e=o()(["\n  fragment InlineExpansionContext_post on Post {\n    id\n    creator {\n      id\n      customStyleSheet {\n        id\n        blogroll {\n          visibility\n        }\n      }\n      isAuroraVisible\n      followedCollections\n      socialStats {\n        followingCount\n        collectionFollowingCount\n      }\n      ...UserSubscribeButton_user\n    }\n    collection {\n      id\n      canToggleEmail\n      description\n      isAuroraEligible\n      isAuroraVisible\n      viewerEdge {\n        id\n        isEditor\n      }\n      tagline\n    }\n    customStyleSheet {\n      id\n      blogroll {\n        visibility\n      }\n    }\n  }\n  ","\n"]);return p=function(){return e},e}var f=s.createContext({expandedPostId:null,setExpandedPostId:function(){},postInView:!1,setPostInView:function(){},expandedPost:null,setExpandedPost:function(){}}),v=function(){return s.useContext(f)},m=function(e){var t=e.children,n=s.useState(null),r=l()(n,2),o=r[0],i=r[1],a=s.useState(!1),d=l()(a,2),p=d[0],v=d[1],m=s.useState(null),b=l()(m,2),h=b[0],E=b[1],C=(0,u.VB)({name:"enable_inline_expansion",placeholder:null});return s.createElement(f.Provider,{value:{expandedPostId:o,setExpandedPostId:i,postInView:p,setPostInView:v,expandedPost:h,setExpandedPost:E}},s.createElement(c.k,{post:h,preload:!!C},t))},b=(0,a.Ps)(p(),d.w)},33819:(e,t,n)=>{"use strict";n.d(t,{h:()=>b});var r=n(59713),o=n.n(r),i=n(67294),l=n(42933),a=n(33914),s=n(98024),c=n(95760),u=n(51512),d=n(6688),p=n(43915),f=n(55459);function v(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function m(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?v(Object(n),!0).forEach((function(t){o()(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):v(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var b=function(e){var t=e.allowResponses,n=e.responsesCount,r=e.handleClick,o=e.trackingData,v=e.isLimitedState,b=e.iconStylesOverride,h=e.countStylesOverride,E=e.svgSize,C=void 0===E?"L":E,y=e.responsesCountColor,P=void 0===y?"LIGHTER":y,w=(0,d.I)(),S=(0,c.Av)(),g=(0,u.pK)();if(!t)return null;var O=function(e){return{fill:e.baseColor.fill.light,opacity:v?.4:1,cursor:v?"not-allowed":"pointer",":hover":{fill:v?void 0:e.baseColor.fill.lighter}}},T={opacity:v?.4:1},I="S"===C?i.createElement(p.Z,{"aria-label":"responses",className:w([O,b])}):i.createElement(f.Z,{"aria-label":"responses",className:w([O,b])}),k=i.createElement("button",{onClick:v?void 0:function(e){r(e),S.event("responses.viewAllClicked",m(m({},o),{},{source:g}))},className:w({cursor:"pointer",border:0,padding:0})},i.createElement(l.x,{display:"flex",flexDirection:"row",alignItems:"center"},i.createElement(l.x,{display:"flex",alignItems:"center"},I,!!n&&i.createElement(s.F,{tag:"p",scale:"M",color:P},i.createElement("span",{className:w([h,T])},n))))),x=i.createElement(a._,{tooltipText:"This feature is temporarily disabled.",targetDistance:15},k);return i.createElement(i.Fragment,null,v?x:k)}},29577:(e,t,n)=>{"use strict";n.d(t,{L:()=>l});var r=n(68356),o=n.n(r),i=n(19725),l=o()({loader:function(){return Promise.all([n.e(8342),n.e(3930),n.e(9068),n.e(8698),n.e(9590),n.e(9845),n.e(7417)]).then(n.bind(n,5758))},modules:["src/components/responses/post/ThreadedResponsesSidebar"],webpack:function(){return[5758]},loading:function(){return null},render:(0,i.n)("ThreadedResponsesSidebar")})},73788:(e,t,n)=>{"use strict";n.d(t,{k:()=>u});var r=n(63038),o=n.n(r),i=n(67294),l=n(49486),a=n(29577),s=n(70586),c=n(92214),u=function(e){var t=e.children,n=e.post,r=e.preload,u=void 0===r||r,d=i.useState(void 0),p=o()(d,2),f=p[0],v=p[1],m=i.useCallback((function(e){return function(t){v(t),e()}}),[]);return i.createElement(s.E,{preload:u},(function(e){var r=e.showPreviousSidebar,o=e.hasLoaded,s=e.initialSidebarRender,u=e.isVisible,d=e.continueThisThreadPosts,p=e.openSidebar,b=e.cleanupSidebar;return i.createElement(l.Q.Provider,{value:{openSidebarToRespondToHighlight:m(p)}},!!n&&o&&i.createElement(a.L,{isResponsesSidebarVisible:u&&0===d.length,parentPost:n,inResponseToQuote:f,setInResponseToQuote:v,showPreviousSidebar:r,cleanupSidebar:b,initialSidebarRender:!!s.current}),!!n&&o&&d.map((function(e,t,o){var l=(0,c.iI)(t);return i.createElement(a.L,{key:n.id,isResponsesSidebarVisible:u&&t===o.length-1,parentPost:n,inResponseToQuote:f,setInResponseToQuote:v,continueThisThreadPost:e,continueThisThreadPostDepth:l,showPreviousSidebar:r,cleanupSidebar:b,initialSidebarRender:!!s.current})})),t)}))}},72393:(e,t,n)=>{"use strict";n.d(t,{f:()=>r});var r=n(67294).createContext({addContinueThisThreadSidebar:function(){return null},openSidebar:function(){return null},closeSidebar:function(){return null}})},70586:(e,t,n)=>{"use strict";n.d(t,{E:()=>m});var r=n(319),o=n.n(r),i=n(63038),l=n.n(i),a=n(38125),s=n.n(a),c=n(67294),u=n(29577),d=n(72393),p=n(77180),f=n(27108),v=n(8403),m=function(e){var t=e.preload,n=e.children,r=c.useState(!1),i=l()(r,2),a=i[0],m=i[1],b=(0,p.F)(),h=!!(0,v.Wd)("responsesOpen"),E=c.useState(!1),C=l()(E,2),y=C[0],P=C[1],w=c.useRef(!0),S=c.useRef(0),g=c.useState(!1),O=l()(g,2),T=O[0],I=O[1],k=c.useCallback((function(){return P(!0)}),[]),x=c.useState([]),R=l()(x,2),j=R[0],D=R[1],V=c.useCallback((function(e){w.current=!1,D([].concat(o()(j),[e]))}),[j]),L=c.useCallback((function(){D(s()(j))}),[j]),F=c.useCallback((function(){P(!1),D([]),w.current=!0}),[]);c.useEffect((function(){I(!0),P(h)}),[h]);var _=function(){window.innerWidth<b.breakpoints.md&&m(!0)};return c.useEffect((function(){return _(),f.V6.on("resize",_),function(){return f.V6.off("resize",_)}}),[]),c.useEffect((function(){var e,t,n=null===(e=window)||void 0===e||null===(t=e.document)||void 0===t?void 0:t.documentElement;return a&&null!=n&&n.style&&(y?(n.style.top="-".concat(S.current,"px"),S.current=n.scrollTop,n.style.overflow="hidden",n.style.position="fixed"):(n.style.overflow="",n.style.position="",n.style.top="",n.scrollTop=S.current)),function(){a&&null!=n&&n.style&&(n.style.overflow="",n.style.position="",n.style.top="",n.scrollTop=S.current)}}),[y]),c.useEffect((function(){t&&u.L.preload()}),[t]),c.createElement(d.f.Provider,{value:{addContinueThisThreadSidebar:V,openSidebar:k,closeSidebar:F}},n({showPreviousSidebar:L,hasLoaded:T,initialSidebarRender:w,isVisible:y,continueThisThreadPosts:j,openSidebar:k,cleanupSidebar:F}))}},32261:(e,t,n)=>{"use strict";n.d(t,{O1:()=>i}),n(59713);var r=n(67294),o=r.createContext(null),i=function(e){var t=e.event,n=e.children;return r.createElement(o.Provider,{value:{event:t}},n)}}}]);
//# sourceMappingURL=https://stats.medium.build/lite/sourcemaps/8607.eb32b1d9.chunk.js.map